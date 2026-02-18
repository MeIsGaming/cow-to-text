from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cowtotext",
    version="1.0.0",
    author="Ashley",
    author_email="info@meisgaming.net",
    description="Real-time audio transcription and translation using Whisper and Argos Translate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MeIsGaming/cow-to-text",
    py_modules=["cowtotext", "cowtotext_main"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cowtotext=cowtotext_main",
        ],
    },
)
