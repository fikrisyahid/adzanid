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
    QSlider,
)
from PyQt6.QtCore import pyqtSignal, Qt

from app.constants import CITIES, DEFAULT_ADHAN_PATH


class SettingsTab(QWidget):
    """Tab widget containing all user-configurable settings."""

    # Signals emitted when the user changes a setting
    city_changed = pyqtSignal(str)
    mp3_path_changed = pyqtSignal(str)
    volume_changed = pyqtSignal(float)
    mute_toggled = pyqtSignal(bool)
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

        # Volume control
        layout.addSpacing(10)
        layout.addWidget(QLabel("Volume Adzan:"))

        volume_layout = QHBoxLayout()
        self.chk_mute = QCheckBox("Mute")
        self.chk_mute.toggled.connect(self._on_mute_toggled)
        volume_layout.addWidget(self.chk_mute)

        self.slider_volume = QSlider(Qt.Orientation.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(100)
        self.slider_volume.setTickInterval(10)
        self.slider_volume.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_volume.valueChanged.connect(self._on_volume_changed)
        volume_layout.addWidget(self.slider_volume, 1)

        self.lbl_volume = QLabel("100%")
        self.lbl_volume.setMinimumWidth(40)
        volume_layout.addWidget(self.lbl_volume)

        layout.addLayout(volume_layout)

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

    def _on_volume_changed(self, value: int):
        """Handle volume slider changes."""
        self.lbl_volume.setText(f"{value}%")
        self.volume_changed.emit(value / 100.0)

    def _on_mute_toggled(self, checked: bool):
        """Handle mute checkbox toggle."""
        self.slider_volume.setEnabled(not checked)
        self.mute_toggled.emit(checked)

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
