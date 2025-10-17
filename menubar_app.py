#!/usr/bin/env python3
"""
Topping E2x2 Menu Bar App
Simple macOS menu bar application for switching audio outputs.
"""
import rumps
from controller import switch_to_headphone, switch_to_speakers, switch_to_both, DeviceError

# Output configuration
HEADPHONE_ICON = "🎧"
SPEAKERS_ICON = "📢"
BOTH_ICON = "✌️"

HEADPHONE_LABEL = f"{HEADPHONE_ICON} Headphones"
SPEAKERS_LABEL = f"{SPEAKERS_ICON} Speakers"
BOTH_LABEL = f"{BOTH_ICON} Both Outputs"


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
            rumps.alert(
                title="Device Error",
                message=str(e),
                ok="OK"
            )

    def switch_to_speakers(self, _):
        """Switch audio output to speakers only."""
        try:
            switch_to_speakers()
            self.current_output = "Speakers"
            self.title = SPEAKERS_ICON
            self._update_checkmarks("speakers")
        except DeviceError as e:
            rumps.alert(
                title="Device Error",
                message=str(e),
                ok="OK"
            )

    def switch_to_both(self, _):
        """Switch audio output to both headphone and speakers."""
        try:
            switch_to_both()
            self.current_output = "Both"
            self.title = BOTH_ICON
            self._update_checkmarks("both")
        except DeviceError as e:
            rumps.alert(
                title="Device Error",
                message=str(e),
                ok="OK"
            )


if __name__ == "__main__":
    app = ToppingToggleApp()
    app.run()
