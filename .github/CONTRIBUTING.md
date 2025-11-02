# Contributing to Raspberry Pi Dashboard

Thank you for your interest in contributing! This is a personal hobby project, but all contributions are welcome.

## 🎯 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Use the bug report template
3. Include system information and logs
4. Provide steps to reproduce

### Suggesting Features

1. Check if the feature has been requested
2. Use the feature request template
3. Explain the use case clearly
4. Consider implementation complexity

### Code Contributions

1. **Fork** the repository
2. **Create a branch** for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly** on actual Raspberry Pi hardware
5. **Commit** with clear messages
6. **Push** and create a Pull Request

## 💻 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/raspberry-pi-dashboard.git
cd raspberry-pi-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py
```

## 📝 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Comment complex logic

## 🧪 Testing

Before submitting:

1. Test on Raspberry Pi hardware
2. Test all modified API endpoints
3. Check for errors in logs
4. Test on mobile devices (if UI changes)
5. Verify GPIO functionality (if GPIO-related)

## 📚 Documentation

- Update relevant documentation in `docs/`
- Add comments to complex code
- Update README if adding major features
- Include examples for new features

## 🎨 UI Changes

- Maintain glassmorphism design language
- Ensure mobile responsiveness
- Test on different screen sizes
- Keep accessibility in mind

## ⚡ GPIO/Hardware Changes

- Test with actual hardware
- Document wiring requirements
- Add safety warnings
- Update wiring guide if needed

## 🚀 Commit Messages

Use clear, descriptive commit messages:

```
Good:
- Add GPIO control for relay modules
- Fix memory leak in stats endpoint
- Update wiring guide with 5V relay instructions

Bad:
- fix bug
- update stuff
- changes
```

## 🔍 Pull Request Process

1. Update the README.md with details of changes if needed
2. Update documentation
3. The PR will be reviewed as soon as possible
4. Address any requested changes
5. Once approved, it will be merged

## 🎉 Recognition

Contributors will be acknowledged in the README and release notes.

## 📞 Questions?

- Open a GitHub Discussion
- Check the documentation in `docs/`
- Review existing issues

---

**Thank you for contributing!** 🎉

