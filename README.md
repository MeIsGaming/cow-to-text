# COW-TO-TEXT LIVE TRANSLATOR 🎤

A real-time audio transcription and translation tool that captures live audio from your system, transcribes it using OpenAI's Whisper model, and translates it to your target language.

## Features

- 🎤 Real-time audio capture from system audio
- 🗣️ Speech-to-text transcription using Faster Whisper
- 🌍 Multi-language translation using Argos Translate
- ⚡ Multi-threaded pipeline for efficient processing
- 🎨 Colored console output for easy reading
- 🔧 Interactive configuration for model size, chunk size, and language selection

## Requirements

- Python 3.11+
- PipeWire/PulsAudio (for audio capture)
- FFmpeg
- CUDA-capable GPU (optional, but recommended for better performance)

## Installation

### Option 1: AUR (Arch Linux Users)
```bash
yay -S cowtotext
# or
paru -S cowtotext
```

### Option 2: Manual Installation from Source
```bash
git clone https://github.com/MeIsGaming/cow-to-text.git
cd cow-to-text
python3.11 -m venv venv_fresh
source venv_fresh/bin/activate
pip install -r requirements.txt
```

### Option 3: Quick Setup (with pip directly)
```bash
git clone https://github.com/MeIsGaming/cow-to-text.git
cd cow-to-text
pip install -r requirements.txt
python3.11 cowtotext.py
```

### System Dependencies
Before installation, ensure you have:
```bash
# Arch Linux
sudo pacman -S python ffmpeg libpulse

# Ubuntu/Debian
sudo apt install python3.11 ffmpeg libpulse0

# Fedora
sudo dnf install python3.11 ffmpeg pulseaudio-libs
```

## Usage

Run the translator:
```bash
python3.11 cowtotext.py
```

The application will prompt you to:
1. Select the Whisper model size (tiny, base, small, medium, large)
2. Choose the audio chunk size (100ms - 2000ms)
3. Select source language
4. Select target language

Once configured, the translator will:
- Capture live audio from your system
- Display transcribed text in the source language
- Display translated text in the target language

**Exit**: Press `Ctrl+C` to stop the translator.

## Configuration Options

### Model Sizes
- **tiny**: Fastest, lower quality
- **base**: Balanced
- **small**: Good quality (works best with pl->en i found out)
- **medium**: High quality
- **large**: Highest quality, slowest

### Supported Languages
- Afrikaans, Arabic, German, English, Spanish, French
- Italian, Japanese, Korean, Polish, Portuguese, Russian, Chinese

## Architecture

The application uses a multi-threaded pipeline:

```
Audio Capture → Transcription Worker → Translation Worker → Output
                (FFmpeg/PulseAudio)   (Faster Whisper)      (Argos)
```

- **Audio Queue**: Raw audio chunks from the system
- **Transcribed Queue**: Transcribed text from Whisper
- **Output Queue**: Final translated text

## Development

To modify or extend the application:
- Edit language support in the `LANGUAGES` dictionary
- Adjust threading pool sizes in worker thread creation
- Customize chunk size and overlap for performance tuning

## License

MIT License

## Contributing

Contributions are welcome! Please create a pull request with your improvements.
