import argostranslate.package
import argostranslate.translate
import numpy as np
import queue
import subprocess
import sys
import threading
import time

from faster_whisper import WhisperModel

# Farben


class Colors:
    HEADER = '\033[96m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    lines = text.split('\n')
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    for line in lines:
        print(f"{Colors.BOLD}{Colors.CYAN}{line:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")


def select_option(prompt, options):
    """Interactive selection with colors"""
    print(f"{Colors.BOLD}{Colors.YELLOW}{prompt}{Colors.RESET}")
    for i, option in enumerate(options, 1):
        print(f"  {Colors.CYAN}{i}{Colors.RESET}. {option}")

    while True:
        try:
            choice = int(
                input(f"\n{Colors.GREEN}Select (1-{len(options)}): {Colors.RESET}"))
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass
        print(f"{Colors.RED}Invalid input!{Colors.RESET}")


print_header("🎤 COW-TO-TEXT LIVE TRANSLATOR 🎤\n by Ashley(info@meisgaming.net)")


def get_active_monitor():
    result = subprocess.run(
        ["pactl", "list", "short", "sources"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    running_monitors = []
    other_monitors = []

    for line in lines:
        parts = line.split()
        if len(parts) < 7:
            continue
        name = parts[1]
        state = parts[6]

        if "monitor" in name:
            if state == "RUNNING":
                running_monitors.append(name)
            else:
                other_monitors.append((name, state))

    if running_monitors:
        return running_monitors[0]
    if other_monitors:
        return other_monitors[0][0]
    return None


active_monitor = get_active_monitor()
if active_monitor is None:
    print(f"{Colors.RED}✗ No active audio device found!{Colors.RESET}")
    exit(1)

print(f"{Colors.GREEN}✓ Audio device found:{Colors.RESET} {Colors.BOLD}{active_monitor}{Colors.RESET}\n")

# -------- INTERACTIVE CONFIG --------
print_header("⚙️  CONFIGURATION")

# Modell Größe
MODEL_SIZES = [
    "tiny (fastest, lower quality)",
    "base",
    "small",
    "medium",
    "large (slowest, best quality)"
]
MODEL_SELECTION = select_option("Select Whisper model size:", MODEL_SIZES)
MODEL_SIZE = MODEL_SELECTION.split()[0]

# Chunk Größe
CHUNK_SIZES = [
    "100ms (very fast)",
    "250ms (fast)",
    "500ms",
    "1000ms (accurate)",
    "2000ms (very accurate)"
]
CHUNK_SELECTION = select_option("Select chunk size:", CHUNK_SIZES)
CHUNK_SIZE_MS = int(CHUNK_SELECTION.split("m")[0])

# Sprachen
LANGUAGES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
}

lang_options = [f"{code} - {name}" for code, name in LANGUAGES.items()]
from_lang_sel = select_option("Select source language:", lang_options)
FROM_LANG = from_lang_sel.split()[0]

to_lang_sel = select_option("Select target language:", lang_options)
TO_LANG = to_lang_sel.split()[0]

# Auto-detect CUDA availability
try:
    import torch
    if torch.cuda.is_available():
        DEVICE = "cuda"
        COMPUTE_TYPE = "float16"
    else:
        DEVICE = "cpu"
        COMPUTE_TYPE = "float32"
except:
    DEVICE = "cpu"
    COMPUTE_TYPE = "float32"

CHUNK_SIZE = 16000 * 2 * (CHUNK_SIZE_MS / 1000)
CHUNK_OVERLAP = 16000 * 2 * 0.25

print(f"\n{Colors.GREEN}✓ Configuration:{Colors.RESET}")
print(f"  • Model: {Colors.BOLD}{MODEL_SIZE}{Colors.RESET}")
print(f"  • Chunk size: {Colors.BOLD}{CHUNK_SIZE_MS}ms{Colors.RESET}")
print(
    f"  • Languages: {Colors.BOLD}{LANGUAGES[FROM_LANG]} → {LANGUAGES[TO_LANG]}{Colors.RESET}")

print_header("🔄 INITIALIZATION")

print(f"{Colors.CYAN}→ Loading Whisper model ({MODEL_SIZE})...{Colors.RESET}",
      end=" ", flush=True)
try:
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
except ValueError as e:
    if "CUDA" in str(e):
        print(
            f"\n{Colors.YELLOW}⚠ CUDA not available, falling back to CPU...{Colors.RESET}")
        DEVICE = "cpu"
        COMPUTE_TYPE = "float32"
        model = WhisperModel(MODEL_SIZE, device=DEVICE,
                             compute_type=COMPUTE_TYPE)
    else:
        raise
print(f"{Colors.GREEN}✓{Colors.RESET}")

print(f"{Colors.CYAN}→ Loading translation model...{Colors.RESET}",
      end=" ", flush=True)
installed_languages = argostranslate.translate.get_installed_languages()
from_lang = next(filter(lambda x: x.code == FROM_LANG, installed_languages))
to_lang = next(filter(lambda x: x.code == TO_LANG, installed_languages))
translator = from_lang.get_translation(to_lang)
print(f"{Colors.GREEN}✓{Colors.RESET}")

# Queues für Pipeline
audio_queue = queue.Queue()
transcribed_queue = queue.Queue()
output_queue = queue.Queue()

chunk_counter = 0
chunk_lock = threading.Lock()


def get_next_chunk_id():
    global chunk_counter
    with chunk_lock:
        chunk_counter += 1
        return chunk_counter


def transcribe_worker():
    """Worker Thread for transcription"""
    while True:
        chunk_id, audio = audio_queue.get()
        if audio is None:
            break

        try:
            segments, _ = model.transcribe(audio, language=FROM_LANG)
            for segment in segments:
                original = segment.text.strip()
                if original:
                    transcribed_queue.put((chunk_id, original))
        except Exception as e:
            print(f"{Colors.RED}Transcription error: {e}{Colors.RESET}")


def translate_worker():
    """Worker Thread for translation"""
    while True:
        chunk_id, original = transcribed_queue.get()
        if original is None:
            break

        try:
            translation = translator.translate(original)
            output_queue.put((original, translation))
        except Exception as e:
            print(f"{Colors.RED}Translation error: {e}{Colors.RESET}")


# Starte Worker Threads
transcribe_threads = [threading.Thread(target=transcribe_worker, daemon=True)]
translate_threads = [threading.Thread(target=translate_worker, daemon=True)]

for t in transcribe_threads + translate_threads:
    t.start()

print(f"{Colors.CYAN}→ Starting audio stream...{Colors.RESET}", end=" ", flush=True)

ffmpeg_cmd = [
    "ffmpeg",
    "-f", "pulse",
    "-i", active_monitor,
    "-ac", "1",
    "-ar", "16000",
    "-f", "s16le",
    "-"
]

process = subprocess.Popen(
    ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
print(f"{Colors.GREEN}✓{Colors.RESET}\n")

print_header("🎙️  LIVE TRANSLATION")
print(f"{Colors.YELLOW}(Press Ctrl+C to exit){Colors.RESET}\n")

buffer = b""
last_chunk_time = time.time()

try:
    while True:
        data = process.stdout.read(4096)
        if not data:
            break

        buffer += data

        if len(buffer) >= int(CHUNK_SIZE):
            # Extract exact chunk size
            chunk_bytes = int(CHUNK_SIZE)
            audio_chunk = buffer[:chunk_bytes]
            audio = np.frombuffer(audio_chunk, np.int16).astype(np.float32) / 32768.0
            
            # Keep overlap for continuity
            overlap_bytes = int(CHUNK_OVERLAP)
            buffer = buffer[chunk_bytes - overlap_bytes:]

            chunk_id = get_next_chunk_id()
            audio_queue.put((chunk_id, audio))
            last_chunk_time = time.time()

        # Output
        while True:
            try:
                original, translation = output_queue.get_nowait()
                print(
                    f"{Colors.BOLD}{Colors.BLUE}[{FROM_LANG.upper()}]{Colors.RESET} {original}")
                print(
                    f"{Colors.BOLD}{Colors.GREEN}[{TO_LANG.upper()}]{Colors.RESET} {translation}")
                print()
                sys.stdout.flush()
            except queue.Empty:
                break

except KeyboardInterrupt:
    print(f"\n{Colors.YELLOW}→ Shutting down...{Colors.RESET}")

finally:
    # Signal zum Beenden
    audio_queue.put((None, None))
    transcribed_queue.put((None, None))

    time.sleep(0.5)

    # Gebe restliche Items aus
    while not output_queue.empty():
        try:
            original, translation = output_queue.get_nowait()
            print(
                f"{Colors.BOLD}{Colors.BLUE}[{FROM_LANG.upper()}]{Colors.RESET} {original}")
            print(
                f"{Colors.BOLD}{Colors.GREEN}[{TO_LANG.upper()}]{Colors.RESET} {translation}")
            print()
        except queue.Empty:
            break

    # ffmpeg beenden
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    # Threads beenden
    for t in transcribe_threads + translate_threads:
        t.join(timeout=0.5)

    print(f"{Colors.GREEN}✓ Program terminated.{Colors.RESET}\n")
