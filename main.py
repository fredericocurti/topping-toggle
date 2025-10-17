#!/usr/bin/env python3
"""
Topping E2x2 CLI Tool
Command-line interface for controlling the Topping E2x2 device.
"""
import sys
from controller import (
    switch_to_headphone,
    switch_to_speakers,
    switch_to_both,
    DeviceError
)


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py [command]")
        print("\nCommands:")
        print("  h  - Headphone only 🎧")
        print("  s  - Speakers only 🔊")
        print("  b  - Both outputs 🎵")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    try:
        if cmd == "h":
            print("🎧 Switching to headphone...")
            switch_to_headphone()
        elif cmd == "s":
            print("🔊 Switching to speakers...")
            switch_to_speakers()
        elif cmd == "b":
            print("🎵 Switching to both outputs...")
            switch_to_both()
        else:
            print(f"Invalid command: {cmd}")
            print("Use: h | s | b")
            sys.exit(1)

        print("✅ Done.")
    except DeviceError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
