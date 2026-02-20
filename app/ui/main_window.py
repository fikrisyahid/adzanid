"""Main application window that coordinates services and UI tabs."""

import datetime
import os

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox, QStyle
from PyQt6.QtCore import QTimer, QSettings
from PyQt6.QtGui import QIcon

from app.constants import APP_TITLE, SETTINGS_ORG, SETTINGS_APP, DEFAULT_ADHAN_PATH, ICON_PATH
from app.services.prayer_time_service import PrayerTimeService
from app.services.audio_service import AudioService
from app.services.theme_manager import ThemeManager
from app.services.startup_service import StartupService
from app.services.update_service import UpdateService
from app.services.dnd_service import is_dnd_enabled
from app.ui.schedule_tab import ScheduleTab
from app.ui.settings_tab import SettingsTab
from app.ui.about_tab import AboutTab
from app.ui.system_tray import SystemTrayManager


class MainWindow(QMainWindow):
    """Top-level window that wires together services, tabs, and the system tray."""

    def __init__(self):
        super().__init__()

        # --- Configuration ---
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(400, 550)
        self.resize(400, 550)
        self._setup_window_icon()

        self._settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        self._prayer_times: dict[str, str] = {}
        self._last_triggered_time: str | None = None
        self._current_date: str | None = None  # Track date to detect day change

        # --- Services ---
        self._prayer_service = PrayerTimeService()
        self._audio_service = AudioService()
        self._audio_service.playback_finished.connect(
            lambda: self._update_audio_buttons(playing=False)
        )
        self._theme_manager = ThemeManager()
        self._startup_service = StartupService()
        self._update_service = UpdateService()

        # Load persisted theme preference before building UI
        self._theme_manager.is_dark = self._settings.value(
            "dark_mode", False, type=bool
        )
        self._theme_manager.apply()

        # --- UI ---
        self._init_tabs()
        self._tray = SystemTrayManager(self)

        # --- Connect signals ---
        self._connect_signals()

        # --- Restore saved settings ---
        self._load_settings()

        # --- Periodic timer (every second) ---
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._timer.start(1000)

        # Fetch initial data
        self._fetch_prayer_times()
        
        # Check for updates
        self._check_for_updates()

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _setup_window_icon(self):
        """Load window icon from file or use system default."""
        if os.path.exists(ICON_PATH):
            icon = QIcon(ICON_PATH)
        else:
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        self.setWindowIcon(icon)

    # ------------------------------------------------------------------
    # UI setup
    # ------------------------------------------------------------------

    def _init_tabs(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self._tabs = QTabWidget()
        layout.addWidget(self._tabs)

        self._schedule_tab = ScheduleTab()
        self._settings_tab = SettingsTab()
        self._about_tab = AboutTab()

        self._tabs.addTab(self._schedule_tab, "Jadwal")
        self._tabs.addTab(self._settings_tab, "Pengaturan")
        self._tabs.addTab(self._about_tab, "Tentang")

    def _connect_signals(self):
        # Settings tab signals → main window handlers
        self._settings_tab.city_changed.connect(self._fetch_prayer_times)
        self._settings_tab.mp3_path_changed.connect(self._on_mp3_path_changed)
        self._settings_tab.dark_mode_toggled.connect(self._on_dark_mode_toggled)
        self._settings_tab.minimize_to_tray_toggled.connect(self._on_minimize_to_tray_toggled)
        self._settings_tab.startup_toggled.connect(self._on_startup_toggled)
        self._settings_tab.test_audio_requested.connect(self._on_test_audio)
        self._settings_tab.stop_audio_requested.connect(self._on_stop_audio)
        self._settings_tab.test_notification_requested.connect(self._on_test_notification)
        self._settings_tab.volume_changed.connect(self._on_volume_changed)
        self._settings_tab.mute_toggled.connect(self._on_mute_toggled)

        # Schedule tab signals
        self._schedule_tab.stop_audio_requested.connect(self._on_stop_audio)

        # System tray signals
        self._tray.show_requested.connect(self._show_window)

    # ------------------------------------------------------------------
    # Settings persistence
    # ------------------------------------------------------------------

    def _load_settings(self):
        saved_city = self._settings.value("city", "Jakarta")
        self._settings_tab.set_city(saved_city)

        saved_mp3 = self._settings.value("mp3_path", DEFAULT_ADHAN_PATH)
        if saved_mp3:
            self._settings_tab.set_mp3_path_label(saved_mp3)

        is_dark = self._settings.value("dark_mode", False, type=bool)
        self._settings_tab.chk_dark.setChecked(is_dark)

        is_tray = self._settings.value("minimize_to_tray", True, type=bool)
        self._settings_tab.chk_tray.setChecked(is_tray)

        is_startup = self._settings.value("startup", False, type=bool)
        self._settings_tab.chk_startup.setChecked(is_startup)

        # Volume & mute
        saved_volume = self._settings.value("volume", 100, type=int)
        self._settings_tab.slider_volume.setValue(saved_volume)
        self._audio_service.volume = saved_volume / 100.0

        is_muted = self._settings.value("muted", False, type=bool)
        self._settings_tab.chk_mute.setChecked(is_muted)
        self._audio_service.muted = is_muted

    def _on_mp3_path_changed(self, path: str):
        self._settings.setValue("mp3_path", path)

    def _on_dark_mode_toggled(self, enabled: bool):
        self._settings.setValue("dark_mode", enabled)
        self._theme_manager.is_dark = enabled
        self._theme_manager.apply()

    def _on_minimize_to_tray_toggled(self, enabled: bool):
        self._settings.setValue("minimize_to_tray", enabled)

    def _on_startup_toggled(self, enabled: bool):
        self._settings.setValue("startup", enabled)
        try:
            self._startup_service.set_startup(enabled)
        except Exception as e:
            QMessageBox.warning(self, "Error Registry", str(e))

    def _on_volume_changed(self, volume: float):
        self._audio_service.volume = volume
        self._settings.setValue("volume", int(volume * 100))

    def _on_mute_toggled(self, muted: bool):
        self._audio_service.muted = muted
        self._settings.setValue("muted", muted)

    # ------------------------------------------------------------------
    # Prayer time fetching
    # ------------------------------------------------------------------

    def _fetch_prayer_times(self):
        city = self._settings_tab.selected_city
        self._settings.setValue("city", city)

        try:
            self._prayer_times = self._prayer_service.fetch(city)
            for name, time_str in self._prayer_times.items():
                self._schedule_tab.set_prayer_time(name, time_str)

            today = PrayerTimeService.today_formatted()
            self._schedule_tab.set_info_text(f"Jadwal {city}, {today}")
        except Exception as e:
            self._schedule_tab.set_info_text("Gagal mengambil data")
            print(e)

    def _check_for_updates(self):
        """Check for application updates from GitHub."""
        result = self._update_service.check_for_updates()
        if result['update_available']:
            self._schedule_tab.show_update_notification(
                result['latest_version'],
                result['download_url']
            )

    # ------------------------------------------------------------------
    # Clock tick & adhan trigger
    # ------------------------------------------------------------------

    def _on_tick(self):
        now = datetime.datetime.now()
        self._schedule_tab.update_clock(now.strftime("%H:%M:%S"))

        # Detect day change and re-fetch prayer times
        today = now.strftime("%d-%m-%Y")
        if self._current_date is not None and self._current_date != today:
            self._current_date = today
            self._last_triggered_time = None
            self._fetch_prayer_times()
            return
        self._current_date = today

        current_short = now.strftime("%H:%M")
        if self._last_triggered_time == current_short:
            return

        for prayer, p_time in self._prayer_times.items():
            if current_short == p_time:
                self._last_triggered_time = current_short
                self._trigger_adhan(prayer)

    def _trigger_adhan(self, prayer_name: str):
        self._tray.notify(
            "Waktu Sholat Tiba",
            f"Saatnya sholat {prayer_name}",
        )
        # Skip audio if system Do Not Disturb / Focus Assist is active
        if is_dnd_enabled():
            return
        self._play_adhan()

    def _play_adhan(self):
        mp3_path = self._settings.value("mp3_path", DEFAULT_ADHAN_PATH)
        if self._audio_service.play(mp3_path):
            self._update_audio_buttons(playing=True)

    def _on_test_audio(self):
        mp3_path = self._settings.value("mp3_path", DEFAULT_ADHAN_PATH)
        if self._audio_service.play(mp3_path):
            self._update_audio_buttons(playing=True)
        else:
            QMessageBox.warning(
                self, "Info", "File MP3 belum dipilih atau tidak ditemukan."
            )

    def _on_stop_audio(self):
        self._audio_service.stop()
        self._update_audio_buttons(playing=False)

    def _on_test_notification(self):
        """Start a 10-second countdown to test the adhan notification."""
        self._settings_tab.btn_test_notification.setEnabled(False)
        self._settings_tab.btn_test_notification.setText("⏰ Menunggu 10 detik...")
        
        # Show immediate notification
        self._tray.notify(
            "Test Notifikasi",
            "Adzan akan berbunyi dalam 10 detik",
            2000,
        )
        
        # Create a single-shot timer for 10 seconds
        QTimer.singleShot(10000, self._on_test_notification_trigger)

    def _on_test_notification_trigger(self):
        """Called after 10 seconds to trigger the test adhan."""
        self._trigger_adhan("Test")
        self._settings_tab.btn_test_notification.setEnabled(True)
        self._settings_tab.btn_test_notification.setText("⏰ Test Notifikasi (10 detik)")

    def _show_window(self):
        """Restore and bring the window to the foreground."""
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def _update_audio_buttons(self, playing: bool):
        self._settings_tab.btn_test.setEnabled(not playing)
        self._settings_tab.btn_stop.setEnabled(playing)
        self._schedule_tab.btn_stop_adzan.setVisible(playing)

    # ------------------------------------------------------------------
    # Window close → tray behaviour
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        if self._settings_tab.minimize_to_tray:
            event.ignore()
            self.hide()
            self._tray.notify(
                "Aplikasi Berjalan",
                "Aplikasi diminimize ke System Tray",
                2000,
            )
        else:
            event.accept()
