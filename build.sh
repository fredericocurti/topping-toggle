#!/bin/bash
# Build script for Topping Toggle macOS app

echo "🔨 Building Topping Toggle..."

# Activate venv
source venv/bin/activate

# Clean previous builds
rm -rf build dist *.spec

# Build with PyInstaller
pyinstaller \
    --name="Topping Toggle" \
    --windowed \
    --onefile \
    --icon=icon.icns \
    --osx-bundle-identifier=com.toppingtoggle.app \
    --clean \
    menubar_app.py

# Update Info.plist to hide from Dock (menu bar only)
/usr/libexec/PlistBuddy -c "Add :LSUIElement bool true" "dist/Topping Toggle.app/Contents/Info.plist" 2>/dev/null || \
/usr/libexec/PlistBuddy -c "Set :LSUIElement true" "dist/Topping Toggle.app/Contents/Info.plist"

echo "🔧 Patched Info.plist to hide from Dock"

# Remove standalone executable (we only need the .app bundle)
rm -f "dist/Topping Toggle"

echo "✅ Build complete!"
echo "📦 App location: dist/Topping Toggle.app"
echo ""
echo "To install: drag 'dist/Topping Toggle.app' to your Applications folder"

