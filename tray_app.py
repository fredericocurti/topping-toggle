#!/usr/bin/env python3
"""
Topping E2x2 System Tray App
Cross-platform system tray application for switching audio outputs.
"""
import sys
import platform
from controller import switch_to_headphone, switch_to_speakers, switch_to_both, DeviceError

# Output configuration
HEADPHONE_ICON = "🎧"
SPEAKERS_ICON = "📢"
BOTH_ICON = "✌️"

HEADPHONE_LABEL = f"{HEADPHONE_ICON} Headphones"
SPEAKERS_LABEL = f"{SPEAKERS_ICON} Speakers"
BOTH_LABEL = f"{BOTH_ICON} Both Outputs"

# Detect platform
IS_MACOS = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"


def show_error(title, message):
    """Show an error dialog appropriate for the platform."""
    if IS_MACOS:
        import rumps
        rumps.alert(title=title, message=message, ok="OK")
    elif IS_WINDOWS:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10 | 0x0)  # MB_ICONERROR | MB_OK
    else:
        print(f"{title}: {message}")


if IS_MACOS:
    # macOS implementation using rumps
    import rumps
    
    class ToppingToggleApp(rumps.App):
        def __init__(self):
            super(ToppingToggleApp, self).__init__(HEADPHONE_ICON, quit_button=None)
            self.current_output = "Headphone"
            
            # Create menu items with keyboard shortcuts
            self.headphone_item = rumps.MenuItem(HEADPHONE_LABEL, callback=self.switch_to_headphone, key="1")
            self.speakers_item = rumps.MenuItem(SPEAKERS_LABEL, callback=self.switch_to_speakers, key="2")
            self.both_item = rumps.MenuItem(BOTH_LABEL, callback=self.switch_to_both, key="3")
            
            self.menu = [
                "Topping E2x2",
                rumps.separator,
                self.headphone_item,
                self.speakers_item,
                self.both_item,
                rumps.separator,
                rumps.MenuItem("Quit", callback=rumps.quit_application)
            ]
            
            # Set headphones as default and apply on startup
            self._update_checkmarks("headphone")
            try:
                switch_to_headphone()
            except DeviceError as e:
                print(f"Could not switch to headphones on startup: {e}")
        
        def _update_checkmarks(self, selected):
            """Update checkmarks to show the currently selected output."""
            self.headphone_item.state = (selected == "headphone")
            self.speakers_item.state = (selected == "speakers")
            self.both_item.state = (selected == "both")

        def switch_to_headphone(self, _):
            """Switch audio output to headphone only."""
            try:
                switch_to_headphone()
                self.current_output = "Headphone"
                self.title = HEADPHONE_ICON
                self._update_checkmarks("headphone")
            except DeviceError as e:
                show_error("Device Error", str(e))

        def switch_to_speakers(self, _):
            """Switch audio output to speakers only."""
            try:
                switch_to_speakers()
                self.current_output = "Speakers"
                self.title = SPEAKERS_ICON
                self._update_checkmarks("speakers")
            except DeviceError as e:
                show_error("Device Error", str(e))

        def switch_to_both(self, _):
            """Switch audio output to both headphone and speakers."""
            try:
                switch_to_both()
                self.current_output = "Both"
                self.title = BOTH_ICON
                self._update_checkmarks("both")
            except DeviceError as e:
                show_error("Device Error", str(e))

elif IS_WINDOWS:
    # Windows implementation using pystray
    import pystray
    from PIL import Image, ImageDraw, ImageFont
    import threading
    import winreg
    import os
    import sys
    
    class ToppingToggleApp:
        def __init__(self):
            self.current_output = "Headphone"
            self.icon = None
            self.menu = None
            self._create_icon()
            self._create_menu()
            
            # Set headphones as default and apply on startup
            try:
                switch_to_headphone()
            except DeviceError as e:
                print(f"Could not switch to headphones on startup: {e}")
        
        def _get_startup_registry_key(self):
            """Get the Windows registry key for startup programs."""
            return winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_READ
            )
        
        def _get_exe_path(self):
            """Get the path to the executable or script."""
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                return sys.executable
            else:
                # Running as script - convert to .exe path if it exists
                script_dir = os.path.dirname(os.path.abspath(__file__))
                exe_path = os.path.join(script_dir, 'dist', 'Topping Toggle.exe')
                if os.path.exists(exe_path):
                    return exe_path
                # Fallback to python script
                return sys.executable
        
        def _is_startup_enabled(self):
            """Check if the app is set to start with Windows."""
            try:
                key = self._get_startup_registry_key()
                try:
                    winreg.QueryValueEx(key, "Topping Toggle")
                    return True
                except FileNotFoundError:
                    return False
                finally:
                    winreg.CloseKey(key)
            except Exception:
                return False
        
        def _enable_startup(self):
            """Add the app to Windows startup."""
            try:
                exe_path = self._get_exe_path()
                key = self._get_startup_registry_key()
                try:
                    winreg.SetValueEx(key, "Topping Toggle", 0, winreg.REG_SZ, f'"{exe_path}"')
                    return True
                finally:
                    winreg.CloseKey(key)
            except Exception as e:
                show_error("Startup Error", f"Could not enable startup: {e}")
                return False
        
        def _disable_startup(self):
            """Remove the app from Windows startup."""
            try:
                key = self._get_startup_registry_key()
                try:
                    winreg.DeleteValue(key, "Topping Toggle")
                    return True
                except FileNotFoundError:
                    # Already disabled
                    return True
                finally:
                    winreg.CloseKey(key)
            except Exception as e:
                show_error("Startup Error", f"Could not disable startup: {e}")
                return False
        
        def _toggle_startup(self, icon=None, item=None):
            """Toggle Windows startup on/off."""
            if self._is_startup_enabled():
                self._disable_startup()
            else:
                self._enable_startup()
            # Update menu to reflect new state
            self._create_menu()
            if self.icon:
                self.icon.menu = self.menu
        
        def _create_icon(self):
            """Create an icon for the system tray."""
            import os
            import sys
            
            # Try multiple possible paths for icon.png
            # When running as script: current directory
            # When running as executable: bundled with exe or same directory as exe
            icon_paths = [
                'icon.png',  # Current directory
                os.path.join(os.path.dirname(sys.executable), 'icon.png'),  # Same dir as exe
                os.path.join(os.path.dirname(__file__), 'icon.png'),  # Same dir as script
                os.path.join(sys._MEIPASS, 'icon.png') if hasattr(sys, '_MEIPASS') else None,  # PyInstaller temp dir
            ]
            
            # Remove None values
            icon_paths = [p for p in icon_paths if p is not None]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        img = Image.open(icon_path)
                        # Convert to RGBA for transparency support
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        
                        # Windows system tray works best with 16x16 or 32x32
                        # Try 32x32 first, but preserve aspect ratio if needed
                        target_size = 32
                        # Resize maintaining aspect ratio
                        img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
                        
                        # Create a square image with transparent background
                        square_img = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
                        # Center the icon
                        x_offset = (target_size - img.width) // 2
                        y_offset = (target_size - img.height) // 2
                        square_img.paste(img, (x_offset, y_offset), img)
                        
                        self.icon_image = square_img
                        return
                    except Exception as e:
                        print(f"Could not load icon from {icon_path}: {e}")
                        continue
            
            # Fallback: Create a simple icon with transparency
            img = Image.new('RGBA', (32, 32), color=(255, 255, 255, 0))  # Transparent background
            draw = ImageDraw.Draw(img)
            # Draw a simple headphone icon
            # Draw a circle for the headphone cup
            draw.ellipse([4, 8, 12, 16], fill=(0, 0, 0, 255), outline=(100, 100, 100, 255), width=1)
            draw.ellipse([20, 8, 28, 16], fill=(0, 0, 0, 255), outline=(100, 100, 100, 255), width=1)
            # Draw the headband
            draw.arc([8, 6, 24, 18], start=180, end=0, fill=(0, 0, 0, 255), width=2)
            self.icon_image = img
        
        def _create_menu(self):
            """Create the system tray menu."""
            startup_enabled = self._is_startup_enabled()
            self.menu = pystray.Menu(
                pystray.MenuItem("Topping E2x2", None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    HEADPHONE_LABEL,
                    self.switch_to_headphone,
                    checked=lambda item: self.current_output == "Headphone",
                    radio=True
                ),
                pystray.MenuItem(
                    SPEAKERS_LABEL,
                    self.switch_to_speakers,
                    checked=lambda item: self.current_output == "Speakers",
                    radio=True
                ),
                pystray.MenuItem(
                    BOTH_LABEL,
                    self.switch_to_both,
                    checked=lambda item: self.current_output == "Both",
                    radio=True
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    "Start with Windows",
                    self._toggle_startup,
                    checked=lambda item: startup_enabled
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit", self.quit_app)
            )
        
        def _update_icon_title(self):
            """Update the icon tooltip based on current output."""
            if self.current_output == "Headphone":
                title = f"Topping Toggle - {HEADPHONE_ICON} Headphones"
            elif self.current_output == "Speakers":
                title = f"Topping Toggle - {SPEAKERS_ICON} Speakers"
            else:
                title = f"Topping Toggle - {BOTH_ICON} Both Outputs"
            
            if self.icon:
                self.icon.title = title
        
        def switch_to_headphone(self, icon=None, item=None):
            """Switch audio output to headphone only."""
            try:
                switch_to_headphone()
                self.current_output = "Headphone"
                self._update_icon_title()
            except DeviceError as e:
                show_error("Device Error", str(e))
        
        def switch_to_speakers(self, icon=None, item=None):
            """Switch audio output to speakers only."""
            try:
                switch_to_speakers()
                self.current_output = "Speakers"
                self._update_icon_title()
            except DeviceError as e:
                show_error("Device Error", str(e))
        
        def switch_to_both(self, icon=None, item=None):
            """Switch audio output to both headphone and speakers."""
            try:
                switch_to_both()
                self.current_output = "Both"
                self._update_icon_title()
            except DeviceError as e:
                show_error("Device Error", str(e))
        
        def quit_app(self, icon=None, item=None):
            """Quit the application."""
            if self.icon:
                self.icon.stop()
        
        def run(self):
            """Run the system tray application."""
            self.icon = pystray.Icon("Topping Toggle", self.icon_image, self._update_icon_title(), self.menu)
            self._update_icon_title()
            self.icon.run()

else:
    # Fallback for other platforms
    class ToppingToggleApp:
        def __init__(self):
            print("System tray not supported on this platform.")
            print("Please use the command-line interface: python main.py [h|s|b]")
            sys.exit(1)
        
        def run(self):
            pass


if __name__ == "__main__":
    app = ToppingToggleApp()
    app.run()

