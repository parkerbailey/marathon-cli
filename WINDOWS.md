# Windows Installation Guide

## One-Line Installation 🚀

### Method 1: Simple Install (Recommended)

Open **Windows Terminal** or **PowerShell** and run:

```powershell
irm https://raw.githubusercontent.com/parkerbailey/marathon-cli/main/install-simple.ps1 | iex
```

### Method 2: Interactive Install

For more options (pipx, user install, global install):

```powershell
irm https://raw.githubusercontent.com/parkerbailey/marathon-cli/main/install.ps1 | iex
```

### Method 3: Direct pip Install

```powershell
pip install git+https://github.com/parkerbailey/marathon-cli.git
```

---

## Prerequisites

### 1. Python 3.8+

Download from [python.org](https://www.python.org/downloads/)

**Important:** Check "Add Python to PATH" during installation!

Verify installation:
```powershell
python --version
```

### 2. Windows Terminal (Recommended)

For best display experience, use **Windows Terminal**:
- Install from [Microsoft Store](https://aka.ms/terminal)
- Or download from [GitHub Releases](https://github.com/microsoft/terminal/releases)

**Why Windows Terminal?**
- ✅ Full ANSI color support
- ✅ Better Unicode character rendering
- ✅ Modern terminal experience

---

## Installation Methods

### Option A: pipx (Isolated - Recommended)

```powershell
# Install pipx
python -m pip install --user pipx
python -m pipx ensurepath

# Restart terminal, then:
pipx install git+https://github.com/parkerbailey/marathon-cli.git
```

**Advantages:**
- ✅ Isolated installation
- ✅ No dependency conflicts
- ✅ Easy to uninstall

### Option B: User Install

```powershell
pip install --user git+https://github.com/parkerbailey/marathon-cli.git
```

**Advantages:**
- ✅ No admin rights needed
- ✅ Only affects your user

### Option C: Global Install

```powershell
# May require admin (Run as Administrator)
pip install git+https://github.com/parkerbailey/marathon-cli.git
```

### Option D: From Wheel (Offline)

If you have the `.whl` file:

```powershell
pip install marathon_cli-0.1.0-py3-none-any.whl
```

---

## After Installation

### Running the CLI

```powershell
marathon-cli
```

### Common Commands

```powershell
# Live monitor (default)
marathon-cli

# Single snapshot
marathon-cli status

# JSON output
marathon-cli status --json

# Player count only
marathon-cli players

# Custom refresh interval
marathon-cli monitor --interval 30
```

---

## Troubleshooting

### "marathon-cli is not recognized"

**Solution 1: Restart Terminal**
Close and reopen Windows Terminal/PowerShell.

**Solution 2: Add Python Scripts to PATH**

1. Find your Python Scripts directory:
   ```powershell
   python -m site --user-site
   ```
   Usually: `C:\Users\YourName\AppData\Roaming\Python\Python3XX\Scripts`

2. Add to PATH:
   - Press `Win + X` → System
   - Advanced system settings → Environment Variables
   - Edit `Path` variable for your user
   - Add: `C:\Users\YourName\AppData\Roaming\Python\Python3XX\Scripts`
   - Click OK and restart terminal

**Solution 3: Use Python Module Syntax**

```powershell
python -m marathon_cli
```

### Colors Not Displaying

1. **Use Windows Terminal** (not cmd.exe)
2. Or enable ANSI in PowerShell:
   ```powershell
   Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1
   ```
3. Or use **WSL** for full Linux compatibility

### Unicode Characters Not Rendering

1. Set terminal font to a Unicode-compatible font:
   - Windows Terminal: Cascadia Code, Consolas
   - Settings → Profiles → Font Face

2. Or use WSL for full support

### Permission Errors

Run PowerShell as Administrator or use `--user` flag:
```powershell
pip install --user git+https://github.com/parkerbailey/marathon-cli.git
```

### pip Not Found

1. Reinstall Python with "Add to PATH" checked
2. Or use full path:
   ```powershell
   python -m pip install git+https://github.com/parkerbailey/marathon-cli.git
   ```

---

## Alternative: WSL (Best Experience)

For the best experience on Windows, use WSL:

```powershell
# Install WSL (Windows 11 or Windows 10 with updates)
wsl --install

# After restart, in WSL:
pip install git+https://github.com/parkerbailey/marathon-cli.git
marathon-cli
```

**WSL Advantages:**
- ✅ Full Linux compatibility
- ✅ Perfect ANSI/Unicode support
- ✅ Native terminal experience

---

## Uninstallation

```powershell
# If installed with pip
pip uninstall marathon-cli

# If installed with pipx
pipx uninstall marathon-cli
```

---

## Testing Your Installation

```powershell
# Check version
marathon-cli --help

# Test with status command
marathon-cli status

# If successful, you'll see the Marathon CLI interface!
```

---

## Support

- **GitHub Issues**: https://github.com/parkerbailey/marathon-cli/issues
- **Requires**: Python 3.8+, Internet connection
- **Works best with**: Windows Terminal, WSL, or PowerShell 7+
