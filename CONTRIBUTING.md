# Contributing to COW-TO-TEXT

Thanks for your interest in contributing! Here are some guidelines to help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/MeIsGaming/cow-to-text.git`
3. Create a virtual environment: `python3.11 -m venv venv_fresh`
4. Activate it: `source venv_fresh/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

## Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test thoroughly
4. Commit with clear messages: `git commit -m "Add feature: description"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request with a description of your changes

## Code Style

- Follow PEP 8 conventions
- Add docstrings to functions
- Keep functions focused and readable

## Reporting Issues

- Check existing issues first
- Provide clear description and reproduction steps
- Include Python version and system info

## Adding Languages

To add support for a new language:

1. Add language code and name to the `LANGUAGES` dictionary in `cowtotext.py`
2. Test that the language is available in both Whisper and Argos Translate
3. Update README.md
4. Create a pull request

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
