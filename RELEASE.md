# Release Guide

## Version 0.1.1 - Cache Fix Release

This release fixes the caching system that was not properly integrated in v0.1.0.

### What's Fixed
- ✅ MCP server now uses cache by default
- ✅ CLI uses cache by default (with `--no-cache` option)
- ✅ Cache properly populates for all search operations
- ✅ Prevents rate limiting from AllTrails

## Publishing to PyPI

### Prerequisites

1. **PyPI Account**: Create account at https://pypi.org/account/register/
2. **API Token**: Generate at https://pypi.org/manage/account/token/
3. **GitHub Secret**: Add token as `PYPI_API_TOKEN` in repository settings

### Method 1: GitHub Actions (Recommended)

#### Using Git Tags:
```bash
# Update version in pyproject.toml first
git add pyproject.toml
git commit -m "Bump version to 0.1.1"
git push

# Create and push tag
git tag v0.1.1
git push origin v0.1.1
```

The GitHub Action will automatically:
1. Build the package
2. Run twine check
3. Upload to PyPI

#### Manual Trigger:
1. Go to GitHub repository → Actions
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Select branch and run

### Method 2: Manual Upload

```bash
# 1. Clean previous builds
rm -rf dist/ build/

# 2. Build package
python -m build

# 3. Check package
twine check dist/*

# 4. Upload to TestPyPI (optional - test first)
twine upload --repository testpypi dist/*

# 5. Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ alltrails-mcp

# 6. Upload to PyPI (production)
twine upload dist/*
```

### Post-Release

1. **Verify on PyPI**: Check https://pypi.org/project/alltrails-mcp/
2. **Test installation**: `pip install alltrails-mcp==0.1.1`
3. **Update README**: Remove "when published" notes
4. **Create GitHub Release**: Add release notes

## Version History

### 0.1.4 (2025-12-02)
- Fixed: Cache now uses user home directory (`~/.cache/alltrails-mcp/`)
- Fixed: Cache is now globally available across all projects
- Added: `alltrails-search cache` command to view cache location and stats
- Added: `alltrails-search cache --clear` to clear cache
- Improved: Platform-aware cache location (XDG Base Directory spec)

### 0.1.3 (2025-12-02)
- Internal version (skipped)

### 0.1.2 (2025-12-02)
- Internal version (skipped)

### 0.1.1 (2025-12-02)
- Fixed: MCP server now uses SQLite cache
- Fixed: CLI uses cache by default
- Added: `--no-cache` and `--force-refresh` CLI flags
- Added: Cache hit/miss logging in MCP server
- Improved: Better cache integration across all components

### 0.1.0 (2025-12-02)
- Initial release
- MCP server for Claude Desktop
- CLI tools (alltrails-mcp, alltrails-search)
- SQLite caching system (not fully integrated)
- All 63 US National Parks supported

## Changelog

See [GitHub Releases](https://github.com/dbrown540/alltrails-mcp-client/releases) for detailed changelog.
