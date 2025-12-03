# Publishing to PyPI

## Quick Start

1. **Install build tools:**
   ```bash
   pip install build twine
   ```

2. **Build the package:**
   ```bash
   python -m build
   ```

3. **Check the distribution:**
   ```bash
   twine check dist/*
   ```

4. **Upload to TestPyPI (optional, for testing):**
   ```bash
   twine upload --repository testpypi dist/*
   ```

5. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```

## Before Publishing

1. **Update version** in `pyproject.toml`
2. **Update your email** in `pyproject.toml` authors section
3. **Review and test** the package locally:
   ```bash
   pip install -e .
   alltrails-search search us/tennessee/great-smoky-mountains-national-park
   ```

## PyPI Account Setup

1. Create an account at https://pypi.org/
2. (Optional) Create a TestPyPI account at https://test.pypi.org/
3. Generate an API token in your account settings
4. Configure credentials in `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN
```

## Version Bumping

Update the version number in `pyproject.toml` following semantic versioning:
- **MAJOR** version for incompatible API changes
- **MINOR** version for added functionality (backwards-compatible)
- **PATCH** version for bug fixes (backwards-compatible)

Example: `0.1.0` → `0.1.1` (bug fix) or `0.2.0` (new feature)
