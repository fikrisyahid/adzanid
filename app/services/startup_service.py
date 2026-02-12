"""Service for managing run-at-startup on Windows, macOS, and Linux."""

import sys
import os
import plistlib

from app.constants import APP_NAME


class StartupService:
    """Manages the 'Run at Startup' feature across platforms."""

    # Windows registry path
    _WIN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # macOS LaunchAgent plist
    _MAC_LABEL = f"com.{APP_NAME}.app"
    _MAC_PLIST_DIR = os.path.expanduser("~/Library/LaunchAgents")
    _MAC_PLIST_PATH = os.path.join(_MAC_PLIST_DIR, f"{_MAC_LABEL}.plist")

    # Linux .desktop autostart
    _LINUX_AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
    _LINUX_DESKTOP_PATH = os.path.join(_LINUX_AUTOSTART_DIR, f"{APP_NAME}.desktop")

    @staticmethod
    def _get_launch_command() -> tuple[str, str]:
        """Return (exe_path, script_path) for launching the app."""
        exe_path = sys.executable
        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "main.py")
        )
        return exe_path, script_path

    def set_startup(self, enabled: bool) -> None:
        """Enable or disable run-at-startup for the current platform.

        Raises:
            OSError: If the platform-specific operation fails.
        """
        if sys.platform == "win32":
            self._set_startup_windows(enabled)
        elif sys.platform == "darwin":
            self._set_startup_macos(enabled)
        elif sys.platform.startswith("linux"):
            self._set_startup_linux(enabled)

    # ------------------------------------------------------------------
    # Windows
    # ------------------------------------------------------------------

    def _set_startup_windows(self, enabled: bool) -> None:
        import winreg

        exe_path, script_path = self._get_launch_command()
        cmd = f'"{exe_path}" "{script_path}"'

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            self._WIN_KEY_PATH,
            0,
            winreg.KEY_ALL_ACCESS,
        )
        try:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
        finally:
            winreg.CloseKey(key)

    # ------------------------------------------------------------------
    # macOS
    # ------------------------------------------------------------------

    def _set_startup_macos(self, enabled: bool) -> None:
        if enabled:
            exe_path, script_path = self._get_launch_command()
            plist_content = {
                "Label": self._MAC_LABEL,
                "ProgramArguments": [exe_path, script_path],
                "RunAtLoad": True,
            }
            os.makedirs(self._MAC_PLIST_DIR, exist_ok=True)
            with open(self._MAC_PLIST_PATH, "wb") as f:
                plistlib.dump(plist_content, f)
        else:
            if os.path.exists(self._MAC_PLIST_PATH):
                os.remove(self._MAC_PLIST_PATH)

    # ------------------------------------------------------------------
    # Linux
    # ------------------------------------------------------------------

    def _set_startup_linux(self, enabled: bool) -> None:
        if enabled:
            exe_path, script_path = self._get_launch_command()
            desktop_entry = (
                "[Desktop Entry]\n"
                f"Name={APP_NAME}\n"
                f"Exec={exe_path} {script_path}\n"
                "Type=Application\n"
                "X-GNOME-Autostart-enabled=true\n"
            )
            os.makedirs(self._LINUX_AUTOSTART_DIR, exist_ok=True)
            with open(self._LINUX_DESKTOP_PATH, "w") as f:
                f.write(desktop_entry)
        else:
            if os.path.exists(self._LINUX_DESKTOP_PATH):
                os.remove(self._LINUX_DESKTOP_PATH)
