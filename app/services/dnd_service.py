"""Service for detecting system Do Not Disturb / Focus Assist state."""

import json
import os
import subprocess
import sys


def is_dnd_enabled() -> bool:
    """Check if the system Do Not Disturb / Focus Assist is active.

    Supports:
    - Windows 10/11: Focus Assist via WNF (Windows Notification Facility)
    - macOS 12+ (Monterey+): Focus mode via ~/Library/DoNotDisturb/DB/Assertions.json
    - macOS < 12: Do Not Disturb via `defaults` command
    - Linux GNOME: via `gsettings org.gnome.desktop.notifications show-banners`
    - Linux KDE Plasma: via D-Bus notification inhibitor check

    Returns:
        True if DND/Focus Assist is active, False otherwise or on error.
    """
    if sys.platform == "win32":
        return _check_dnd_windows()
    elif sys.platform == "darwin":
        return _check_dnd_macos()
    elif sys.platform.startswith("linux"):
        return _check_dnd_linux()
    return False


# ------------------------------------------------------------------
# Windows
# ------------------------------------------------------------------

def _check_dnd_windows() -> bool:
    """Focus Assist state via WNF (Windows Notification Facility).

    Values:
        0 = Off, 1 = Priority Only, 2 = Alarms Only
    """
    try:
        import ctypes

        ntdll = ctypes.WinDLL("ntdll", use_last_error=True)

        # WNF_SHEL_QUIETHOURS_ACTIVE_PROFILE_CHANGED state name
        wnf_state_name = (ctypes.c_uint32 * 2)(0xA3BF1F75, 0x0D83063E)

        changestamp = ctypes.c_uint32(0)
        buffer = (ctypes.c_uint8 * 4)()
        buffer_size = ctypes.c_uint32(4)

        status = ntdll.NtQueryWnfStateData(
            ctypes.byref(wnf_state_name),
            None,
            None,
            ctypes.byref(changestamp),
            ctypes.byref(buffer),
            ctypes.byref(buffer_size),
        )

        if status == 0:  # STATUS_SUCCESS
            value = int.from_bytes(
                bytes(buffer[: buffer_size.value]), byteorder="little"
            )
            return value != 0

    except Exception as e:
        print(f"DND check (Windows) failed: {e}")

    return False


# ------------------------------------------------------------------
# macOS
# ------------------------------------------------------------------

def _check_dnd_macos() -> bool:
    """Detect DND/Focus state on macOS.

    macOS 12+ (Monterey+) stores active Focus assertions in a JSON file.
    Older macOS exposes a `doNotDisturb` defaults key.
    """
    # --- macOS 12+ : Focus / DND via Assertions.json ---
    assertions_path = os.path.expanduser(
        "~/Library/DoNotDisturb/DB/Assertions.json"
    )
    if os.path.exists(assertions_path):
        try:
            with open(assertions_path, "r") as f:
                data = json.load(f)
            # data["data"] is a list; first element holds storeAssertionRecords
            records = (
                data.get("data", [{}])[0].get("storeAssertionRecords", [])
            )
            return len(records) > 0
        except Exception as e:
            print(f"DND check (macOS 12+ assertions) failed: {e}")

    # --- macOS < 12 : legacy doNotDisturb defaults key ---
    try:
        result = subprocess.run(
            [
                "defaults",
                "-currentHost",
                "read",
                "com.apple.notificationcenterui",
                "doNotDisturb",
            ],
            capture_output=True,
            text=True,
            timeout=3,
        )
        return result.stdout.strip() == "1"
    except Exception as e:
        print(f"DND check (macOS legacy) failed: {e}")

    return False


# ------------------------------------------------------------------
# Linux
# ------------------------------------------------------------------

def _check_dnd_linux() -> bool:
    """Detect DND state on Linux (GNOME and KDE Plasma).

    Tries GNOME first (gsettings), then KDE (D-Bus inhibitor query).
    Returns False for other desktop environments.
    """
    # --- GNOME ---
    # show-banners = false  →  DND is ON
    try:
        result = subprocess.run(
            [
                "gsettings",
                "get",
                "org.gnome.desktop.notifications",
                "show-banners",
            ],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode == 0:
            return result.stdout.strip().lower() == "false"
    except Exception:
        pass

    # --- KDE Plasma ---
    # Query the NotificationManager D-Bus service for the inhibited state.
    try:
        result = subprocess.run(
            [
                "dbus-send",
                "--session",
                "--print-reply",
                "--dest=org.kde.plasmashell",
                "/org/kde/notifications",
                "org.freedesktop.DBus.Properties.Get",
                "string:org.kde.NotificationManager",
                "string:DoNotDisturb",
            ],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode == 0 and "true" in result.stdout.lower():
            return True
    except Exception:
        pass

    return False
