# How to Run Topping Toggle on Windows

## Quick Start - Run from Source

1. **Open PowerShell** in the project directory

2. **Create virtual environment** (first time only):
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```powershell
   venv\Scripts\Activate.ps1
   ```
   
   If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the app**:
   ```powershell
   python tray_app.py
   ```
   
   The app will appear in your system tray (near the clock). Right-click the icon to switch outputs.

## Build Standalone Executable

To create a `.exe` file you can run without Python:

1. **Make sure you've completed steps 1-4 above** (create venv, activate, install dependencies)

2. **Run the build script**:
   ```powershell
   .\build.ps1
   ```

3. **Find your executable**:
   - Location: `dist\Topping Toggle.exe`
   - You can run it directly or copy it anywhere you want

## Command Line Usage

You can also use the command-line interface:

```powershell
# Activate venv first
venv\Scripts\Activate.ps1

# Switch to headphones
python main.py h

# Switch to speakers
python main.py s

# Switch to both outputs
python main.py b
```

## Troubleshooting

- **"Could not open device" error**: Make sure ToppingPro is closed, and try running as Administrator
- **Execution policy error**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Module not found**: Make sure you activated the virtual environment and installed requirements

