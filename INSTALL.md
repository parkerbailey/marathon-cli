# Installation Guide

## Quick Install (Recommended)

### From PyPI (when published)

```bash
pip install marathon-cli
```

### From Source

```bash
git clone https://github.com/parkerbailey/marathon-cli.git
cd marathon-cli
pip install .
```

After installation, simply run:

```bash
marathon-cli
```

---

## Installation Methods

### Method 1: Global Installation (Recommended for general use)

Install globally using `pipx` (recommended) or `pip`:

**Using pipx (isolated installation):**
```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install marathon-cli
pipx install marathon-cli
```

**Using pip:**
```bash
pip install --user marathon-cli
# or
sudo pip install marathon-cli  # system-wide
```

### Method 2: Development Installation

For development or if you want to modify the code:

```bash
# Clone repository
git clone https://github.com/parkerbailey/marathon-cli.git
cd marathon-cli

# Create virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### Method 3: Virtual Environment Installation

For isolated installation without affecting system Python:

```bash
# Create a directory for marathon-cli
mkdir -p ~/.local/share/marathon-cli
cd ~/.local/share/marathon-cli

# Clone and install
git clone https://github.com/parkerbailey/marathon-cli.git .
python3 -m venv venv
source venv/bin/activate
pip install .

# Create a wrapper script
cat > ~/.local/bin/marathon-cli << 'EOF'
#!/bin/bash
~/.local/share/marathon-cli/venv/bin/marathon-cli "$@"
EOF

chmod +x ~/.local/bin/marathon-cli
```

Make sure `~/.local/bin` is in your PATH:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## Building Distribution Packages

### Build wheel and source distribution

```bash
# Install build tools
pip install build twine

# Build packages
python -m build

# This creates:
# - dist/marathon_cli-0.1.0-py3-none-any.whl
# - dist/marathon-cli-0.1.0.tar.gz
```

### Install from local wheel

```bash
pip install dist/marathon_cli-0.1.0-py3-none-any.whl
```

### Upload to PyPI (for maintainers)

```bash
# Test PyPI (optional)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

---

## Verifying Installation

After installation, verify it works:

```bash
# Check version and help
marathon-cli --help

# Test with status command
marathon-cli status

# Run live monitor
marathon-cli
```

---

## Uninstallation

```bash
# If installed with pip
pip uninstall marathon-cli

# If installed with pipx
pipx uninstall marathon-cli
```

---

## Troubleshooting

### Command not found

If you get "command not found" after installation:

1. **Check if the script is installed:**
   ```bash
   python3 -m pip show marathon-cli
   ```

2. **Check your PATH:**
   ```bash
   echo $PATH
   ```

3. **Find where pip installs scripts:**
   ```bash
   python3 -m site --user-base
   # Add /bin to this path and add to your PATH
   ```

4. **Add to PATH (if needed):**
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Import errors

If you get import errors, ensure dependencies are installed:

```bash
pip install requests click pyfiglet
```

### Permission errors

If you get permission errors:

- Use `--user` flag: `pip install --user marathon-cli`
- Or use a virtual environment
- Or use `pipx`

---

## System Requirements

- Python 3.8 or higher
- Terminal with ANSI color support
- Internet connection (for API calls)

### Platform Support

- ✅ Linux
- ✅ macOS
- ⚠️ Windows (may have limited ANSI support in older terminals; use Windows Terminal or WSL)

---

## Dependencies

Automatically installed:
- `requests` (>=2.31.0) - HTTP requests
- `click` (>=8.1.0) - CLI framework
- `pyfiglet` (>=0.8.0) - ASCII art
