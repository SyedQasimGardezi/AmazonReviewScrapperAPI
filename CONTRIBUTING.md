# Contributing to Amazon Review Scraper API

Thank you for your interest in contributing to the Amazon Review Scraper API! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/amazon-review-scraper-api.git
   cd amazon-review-scraper-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

## 🧪 Testing

Run the test suite:
```bash
python test_api.py
```

## 📝 Code Style

We use Black for code formatting and flake8 for linting:

```bash
# Format code
black .

# Check linting
flake8 .
```

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Detailed steps to reproduce the problem
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: Python version, OS, etc.
6. **Screenshots**: If applicable

## 🔧 Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Run tests** to ensure everything works
6. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request**

### Pull Request Guidelines

- Use clear, descriptive commit messages
- Keep PRs focused on a single feature/fix
- Include tests for new functionality
- Update documentation if needed
- Ensure all tests pass

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write clear, self-documenting code
- Add docstrings for functions and classes

### Testing

- Write tests for new features
- Ensure existing tests still pass
- Test edge cases and error conditions

### Documentation

- Update README.md for significant changes
- Add docstrings for new functions
- Update API documentation if needed

## 🏗️ Project Structure

```
amazon-review-scraper-api/
├── amazon_review_api.py    # Main API
├── api_server.py           # Flask server
├── test_api.py            # Test script
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
├── pyproject.toml        # Modern Python packaging
├── README.md             # Documentation
├── CONTRIBUTING.md       # This file
├── LICENSE               # MIT License
└── .gitignore           # Git ignore rules
```

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the code of conduct

## 📞 Getting Help

- Check existing issues first
- Create a new issue for bugs or feature requests
- Join discussions in the community

## 🎯 Areas for Contribution

- **Bug fixes**: Fix existing issues
- **New features**: Add new functionality
- **Documentation**: Improve documentation
- **Tests**: Add more test coverage
- **Performance**: Optimize scraping speed
- **Error handling**: Improve error handling
- **UI/UX**: Improve API usability

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
