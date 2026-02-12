"""Settings tab for city selection, audio, theme, and startup options."""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QCheckBox,
    QFileDialog,
)
from PyQt6.QtCore import pyqtSignal

from app.constants import CITIES, DEFAULT_ADHAN_PATH


class SettingsTab(QWidget):
    """Tab widget containing all user-configurable settings."""

    # Signals emitted when the user changes a setting
    city_changed = pyqtSignal(str)
    mp3_path_changed = pyqtSignal(str)
    dark_mode_toggled = pyqtSignal(bool)
    startup_toggled = pyqtSignal(bool)
    minimize_to_tray_toggled = pyqtSignal(bool)
    test_audio_requested = pyqtSignal()
    stop_audio_requested = pyqtSignal()
    test_notification_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # 1. City selection
        layout.addWidget(QLabel("Pilih Kota:"))
        self.combo_city = QComboBox()
        self.combo_city.addItems(CITIES)
        self.combo_city.currentTextChanged.connect(self.city_changed.emit)
        layout.addWidget(self.combo_city)

        layout.addSpacing(10)

        # 2. MP3 file selection
        layout.addWidget(QLabel("File Suara Adzan:"))
        file_layout = QHBoxLayout()
        self.lbl_mp3_path = QLabel(DEFAULT_ADHAN_PATH)
        self.lbl_mp3_path.setWordWrap(True)
        btn_browse = QPushButton("Cari MP3...")
        btn_browse.clicked.connect(self._browse_mp3)

        file_layout.addWidget(self.lbl_mp3_path)
        file_layout.addWidget(btn_browse)
        layout.addLayout(file_layout)

        # Test / Stop audio buttons
        layout.addSpacing(5)
        audio_btn_layout = QHBoxLayout()

        self.btn_test = QPushButton("▶ Play Adzan")
        self.btn_test.clicked.connect(self.test_audio_requested.emit)
        audio_btn_layout.addWidget(self.btn_test)

        self.btn_stop = QPushButton("⬛ Stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_audio_requested.emit)
        audio_btn_layout.addWidget(self.btn_stop)

        layout.addLayout(audio_btn_layout)

        # Test notification button
        layout.addSpacing(5)
        self.btn_test_notification = QPushButton("⏰ Test Notifikasi (10 detik)")
        self.btn_test_notification.setStyleSheet("padding: 8px;")
        self.btn_test_notification.clicked.connect(self.test_notification_requested.emit)
        layout.addWidget(self.btn_test_notification)

        layout.addSpacing(20)

        # 3. Feature checkboxes
        self.chk_dark = QCheckBox("Dark Mode")
        self.chk_dark.toggled.connect(self.dark_mode_toggled.emit)
        layout.addWidget(self.chk_dark)

        self.chk_tray = QCheckBox("Minimize to Tray when Closed")
        self.chk_tray.toggled.connect(self.minimize_to_tray_toggled.emit)
        layout.addWidget(self.chk_tray)

        self.chk_startup = QCheckBox("Run at Startup")
        self.chk_startup.toggled.connect(self.startup_toggled.emit)
        layout.addWidget(self.chk_startup)

        layout.addStretch()
        self.setLayout(layout)

    def _browse_mp3(self):
        """Open a file dialog to select an adhan audio file."""
        file, _ = QFileDialog.getOpenFileName(
            self, "Pilih File Adzan", "", "Audio Files (*.mp3 *.wav)"
        )
        if file:
            self.lbl_mp3_path.setText(file)
            self.mp3_path_changed.emit(file)

    # --- Public accessors for MainWindow to read/write state ---

    @property
    def selected_city(self) -> str:
        return self.combo_city.currentText()

    def set_city(self, city: str):
        idx = self.combo_city.findText(city)
        if idx >= 0:
            self.combo_city.setCurrentIndex(idx)

    def set_mp3_path_label(self, path: str):
        self.lbl_mp3_path.setText(path)

    @property
    def minimize_to_tray(self) -> bool:
        return self.chk_tray.isChecked()
