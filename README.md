# Topping Toggle

A simple macOS menu bar app to switch audio output between headphones and speakers on your Topping E2x2 device.

<img src="demo.png" alt="Topping Toggle Demo" width="400">

## Features

- 🎧 Quick switch to headphones only
- 📢 Quick switch to speakers only
- ✌️ Quick switch to both outputs
- Clean menu bar interface with custom icon
- Visual indicator of current output
- Keyboard shortcuts: `⌘1/2/3` when menu is open

## Installation

1. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Menu Bar App (Recommended)

```bash
cd /Users/fcurto/toppingtoggle
source venv/bin/activate
python menubar_app.py &
```

Look for the icon in your menu bar (🎧/📢/✌️) and click it to switch outputs.

**Keyboard Shortcuts:**

- `⌘1` - Switch to headphones (when menu is open)
- `⌘2` - Switch to speakers (when menu is open)
- `⌘3` - Switch to both outputs (when menu is open)

### Command Line

```bash
source venv/bin/activate
python main.py [command]
```

Commands:

- `h` - Headphone only 🎧
- `s` - Speakers only 🔊
- `b` - Both outputs 🎵

## Building the App

To rebuild the macOS application:

```bash
./build.sh
```

The app will be created in `dist/Topping Toggle.app`. Drag it to your Applications folder to install.

## Important Notes

⚠️ **Close ToppingPro before running this app!**

macOS only allows one application to access a HID device at a time. Make sure ToppingPro or any other Topping software is closed before using this tool.

## Device Info

- Vendor ID: `0x152A`
- Product ID: `0x8756`
- Product: Topping E2x2 OTG

## Requirements

- macOS
- Python 3.x
- Topping E2x2 device connected
