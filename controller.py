"""
Topping E2x2 Device Controller
Handles all HID communication with the device.
"""
import hid
import time

VENDOR_ID = 0x152A
PRODUCT_ID = 0x8756

# --- Headphone Only ---
HEADPHONE_ONLY = [
    bytes.fromhex("22 33 20 01 01 37 01 00 00 00 01 00 00 66 77 00"),
    bytes.fromhex("22 33 20 01 01 37 03 00 00 00 01 00 00 66 77 00"),
    bytes.fromhex("22 33 20 01 01 37 05 00 00 00 00 00 00 66 77 00"),  # 05=00 for headphone routing
    bytes.fromhex("22 33 20 01 31 03 02 00 00 00 00 00 00 66 77 00"),
    bytes.fromhex("22 33 20 01 32 03 02 00 00 00 00 00 00 66 77 00"),
]

# --- Speakers Only ---
SPEAKERS_ONLY = [
    bytes.fromhex("22 33 20 01 01 37 01 00 00 00 00 00 00 66 77 00"),  # 01=00 mute headphone channel
    bytes.fromhex("22 33 20 01 01 37 03 00 00 00 00 00 00 66 77 00"),  # 03=00 mute headphone channel
    bytes.fromhex("22 33 20 01 01 37 05 00 00 00 01 00 00 66 77 00"),  # 05=01 for speaker routing
    bytes.fromhex("22 33 20 01 31 03 02 00 00 00 00 00 00 66 77 00"),
    bytes.fromhex("22 33 20 01 32 03 02 00 00 00 00 00 00 66 77 00"),
]

# --- Both Outputs ---
BOTH_OUTPUTS = [
    bytes.fromhex("22 33 20 01 01 37 01 00 00 00 01 00 00 66 77 00"),  # 01=01 unmute headphone
    bytes.fromhex("22 33 20 01 01 37 03 00 00 00 01 00 00 66 77 00"),  # 03=01 unmute headphone
    bytes.fromhex("22 33 20 01 01 37 05 00 00 00 01 00 00 66 77 00"),  # 05=01 enable speakers
    bytes.fromhex("22 33 20 01 31 03 02 00 00 00 00 00 00 66 77 00"),
    bytes.fromhex("22 33 20 01 32 03 02 00 00 00 00 00 00 66 77 00"),
]


class DeviceError(Exception):
    """Custom exception for device communication errors."""
    pass


def _send_payload(payload):
    """Send a single HID payload to the device."""
    device = hid.device()
    try:
        device.open(VENDOR_ID, PRODUCT_ID)
    except OSError:
        import platform
        if platform.system() == "Windows":
            raise DeviceError(
                "Could not open device. Possible causes:\n"
                "  • ToppingPro or other software is using the device\n"
                "  • Device is not connected\n"
                "  • Run as Administrator if permission issues occur"
            )
        else:
            raise DeviceError(
                "Could not open device. Possible causes:\n"
                "  • ToppingPro or other software is using the device\n"
                "  • Device is not connected\n"
                "  • Permission issues (try sudo)"
            )
    try:
        device.write(b"\x00" + payload)
        time.sleep(0.05)
    finally:
        device.close()


def _send_sequence(payloads):
    """Send a sequence of payloads."""
    for payload in payloads:
        _send_payload(payload)


def switch_to_headphone():
    """Switch audio output to headphone only."""
    _send_sequence(HEADPHONE_ONLY)


def switch_to_speakers():
    """Switch audio output to speakers only."""
    _send_sequence(SPEAKERS_ONLY)


def switch_to_both():
    """Switch audio output to both headphone and speakers simultaneously."""
    _send_sequence(BOTH_OUTPUTS)
