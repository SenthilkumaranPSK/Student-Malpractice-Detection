# 🤝 Contributing to ExamGuard

First off, thank you for considering contributing to ExamGuard! It's people like you that make ExamGuard such a great tool for ensuring exam integrity.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@examguard.com.

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

---

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Description:**
A clear and concise description of the bug.

**To Reproduce:**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What you expected to happen.

**Screenshots:**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- Browser: [e.g., Chrome 96]

**Additional Context:**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case**: Why is this enhancement useful?
- **Proposed solution**: How should it work?
- **Alternatives**: What other solutions have you considered?
- **Additional context**: Screenshots, mockups, etc.

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `documentation` - Documentation improvements

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- Webcam (for testing)
- Code editor (VS Code recommended)

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click the 'Fork' button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/exam-guard.git
   cd exam-guard
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/original-owner/exam-guard.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

6. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

### Development Dependencies

Create `requirements-dev.txt`:
```
pytest>=7.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
pylint>=2.12.0
mypy>=0.950
pre-commit>=2.17.0
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Run tests**
   ```bash
   pytest tests/
   ```

3. **Check code style**
   ```bash
   black .
   flake8 .
   pylint main.py
   ```

4. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update CHANGELOG.md

### Submitting the PR

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested this with a webcam

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Fixes #(issue number)
```

### Review Process

1. At least one maintainer must approve
2. All CI checks must pass
3. No merge conflicts
4. Code coverage should not decrease

---

## 💻 Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Single quotes for strings, double for docstrings
- **Imports**: Grouped and sorted (use `isort`)

### Code Formatting

Use **Black** for automatic formatting:
```bash
black --line-length 100 .
```

### Naming Conventions

```python
# Classes: PascalCase
class MalpracticeDetector:
    pass

# Functions/Methods: snake_case
def detect_objects(frame):
    pass

# Constants: UPPER_SNAKE_CASE
MAX_DETECTION_CONFIDENCE = 0.95

# Private methods: _leading_underscore
def _internal_helper():
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def detect_objects(frame, confidence_threshold=0.5):
    """
    Detect objects in the given frame using YOLO model.
    
    Args:
        frame (np.ndarray): Input image frame in BGR format
        confidence_threshold (float): Minimum confidence for detection (0-1)
        
    Returns:
        list: List of detection dictionaries containing:
            - type (str): Detection type
            - class (str): Object class name
            - bbox (list): Bounding box coordinates [x, y, w, h]
            - confidence (float): Detection confidence score
            
    Raises:
        ValueError: If frame is None or empty
        
    Example:
        >>> frame = cv2.imread('test.jpg')
        >>> detections = detect_objects(frame, 0.7)
        >>> print(len(detections))
        3
    """
    pass
```

### Type Hints

Use type hints for better code clarity:

```python
from typing import List, Dict, Optional, Tuple

def process_detections(
    detections: List[Dict[str, any]], 
    threshold: float = 0.5
) -> Tuple[int, List[str]]:
    """Process detection results."""
    pass
```

---

## 🧪 Testing Guidelines

### Writing Tests

Create tests in the `tests/` directory:

```python
# tests/test_detection.py
import pytest
from main import MalpracticeDetector

def test_detector_initialization():
    """Test that detector initializes correctly."""
    detector = MalpracticeDetector()
    assert detector is not None
    assert detector.object_model is not None

def test_object_detection():
    """Test object detection functionality."""
    detector = MalpracticeDetector()
    # Add test logic
    pass

@pytest.mark.parametrize("confidence,expected", [
    (0.5, True),
    (0.9, True),
    (0.0, False),
])
def test_confidence_threshold(confidence, expected):
    """Test confidence threshold validation."""
    # Add test logic
    pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_detection.py

# Run specific test
pytest tests/test_detection.py::test_detector_initialization
```

### Test Coverage

- Aim for **80%+ code coverage**
- All new features must include tests
- Bug fixes should include regression tests

---

## 📚 Documentation

### Code Documentation

- Add docstrings to all public functions/classes
- Include usage examples in docstrings
- Keep comments concise and meaningful
- Update inline comments when changing code

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Configuration options
- Dependencies

### Changelog

Update `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [Unreleased]

### Added
- New feature X that does Y

### Changed
- Modified behavior of Z

### Fixed
- Bug in component A

### Removed
- Deprecated feature B
```

---

## 🎨 UI/UX Contributions

### Design Guidelines

- Follow the existing design system in `static/css/style.css`
- Use CSS variables for colors and spacing
- Ensure responsive design (mobile, tablet, desktop)
- Test in multiple browsers (Chrome, Firefox, Safari, Edge)
- Maintain accessibility (WCAG 2.1 AA compliance)

### Adding New UI Components

1. Design mockup (Figma, Adobe XD, or similar)
2. Get feedback from maintainers
3. Implement with existing design tokens
4. Test responsiveness
5. Add to component documentation

---

## 🐛 Debugging Tips

### Common Issues

1. **Camera not working**
   ```python
   # Test camera access
   import cv2
   cap = cv2.VideoCapture(0)
   print(cap.isOpened())
   ```

2. **Model loading errors**
   ```python
   # Verify model file
   import os
   print(os.path.exists('yolov8n.pt'))
   ```

3. **Memory leaks**
   ```python
   # Use memory profiler
   from memory_profiler import profile
   
   @profile
   def your_function():
       pass
   ```

---

## 📞 Getting Help

- 💬 **Discord**: [Join our community](https://discord.gg/examguard)
- 📧 **Email**: dev@examguard.com
- 📖 **Docs**: [docs.examguard.com](https://docs.examguard.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/original-owner/exam-guard/issues)

---

## 🏆 Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in the README
- Invited to our contributors Discord channel

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to ExamGuard! Together, we're making online education more secure and fair.** 🎓✨
