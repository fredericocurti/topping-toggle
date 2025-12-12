# Build script for Topping Toggle Windows app

Write-Host "🔨 Building Topping Toggle..." -ForegroundColor Cyan

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
Remove-Item -Path "build" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "dist" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "*.spec" -ErrorAction SilentlyContinue

# Build with PyInstaller
Write-Host "Building with PyInstaller..." -ForegroundColor Yellow
pyinstaller `
    --name="Topping Toggle" `
    --windowed `
    --onefile `
    --icon=icon.png `
    --clean `
    --noconsole `
    tray_app.py

Write-Host "✅ Build complete!" -ForegroundColor Green
Write-Host "📦 Executable location: dist\Topping Toggle.exe" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run 'dist\Topping Toggle.exe' or copy it to your desired location." -ForegroundColor Cyan

