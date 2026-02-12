"""Schedule tab displaying current time and prayer times."""

import webbrowser

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

from app.constants import PRAYER_NAMES


class ScheduleTab(QWidget):
    """Tab widget that shows the clock and today's prayer schedule."""

    stop_audio_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._prayer_labels: dict[str, QLabel] = {}
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Update notification banner (hidden by default)
        self._update_widget = QFrame()
        self._update_widget.setStyleSheet(
            "background-color: #3498db; border-radius: 8px; padding: 10px;"
        )
        self._update_widget.setVisible(False)
        
        update_layout = QHBoxLayout(self._update_widget)
        update_layout.setContentsMargins(10, 10, 10, 10)
        
        self._lbl_update = QLabel("")
        self._lbl_update.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self._lbl_update.setWordWrap(True)
        update_layout.addWidget(self._lbl_update, 1)
        
        self._btn_download_update = QPushButton("⬇ Download")
        self._btn_download_update.setStyleSheet(
            "background-color: #2ecc71; color: white; font-size: 14px; "
            "font-weight: bold; padding: 8px 16px; border-radius: 5px;"
        )
        self._btn_download_update.clicked.connect(self._on_download_update)
        update_layout.addWidget(self._btn_download_update)
        
        layout.addWidget(self._update_widget)
        layout.addSpacing(10)

        # Large clock header
        self.lbl_current_time = QLabel("00:00:00")
        self.lbl_current_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_current_time.setStyleSheet("font-size: 40px; font-weight: bold;")
        layout.addWidget(self.lbl_current_time)

        self.lbl_info = QLabel("Menunggu jadwal...")
        self.lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_info)

        layout.addSpacing(20)

        # Prayer time rows
        for name in PRAYER_NAMES:
            row = QHBoxLayout()
            lbl_name = QLabel(name)
            lbl_time = QLabel("--:--")
            lbl_name.setStyleSheet("font-size: 16px;")
            lbl_time.setStyleSheet("font-size: 16px; font-weight: bold;")

            row.addWidget(lbl_name)
            row.addStretch()
            row.addWidget(lbl_time)

            layout.addLayout(row)
            self._prayer_labels[name] = lbl_time

        # Stop adzan button (hidden by default)
        self.btn_stop_adzan = QPushButton("⏹ Stop Adzan")
        self.btn_stop_adzan.setStyleSheet(
            "font-size: 16px; padding: 10px; background-color: #c0392b; color: white; border-radius: 6px;"
        )
        self.btn_stop_adzan.setVisible(False)
        self.btn_stop_adzan.clicked.connect(self.stop_audio_requested.emit)
        layout.addWidget(self.btn_stop_adzan)

        layout.addStretch()
        self.setLayout(layout)

    def update_clock(self, time_str: str):
        """Update the large clock display."""
        self.lbl_current_time.setText(time_str)

    def set_info_text(self, text: str):
        """Update the info label below the clock."""
        self.lbl_info.setText(text)

    def set_prayer_time(self, prayer_name: str, time_str: str):
        """Update the displayed time for a specific prayer."""
        if prayer_name in self._prayer_labels:
            self._prayer_labels[prayer_name].setText(time_str)

    def show_update_notification(self, latest_version: str, download_url: str):
        """Show the update notification banner."""
        self._lbl_update.setText(f"🎉 Update tersedia: v{latest_version}")
        self._download_url = download_url
        self._update_widget.setVisible(True)

    def hide_update_notification(self):
        """Hide the update notification banner."""
        self._update_widget.setVisible(False)

    def _on_download_update(self):
        """Open the download URL in the default browser."""
        if hasattr(self, '_download_url'):
            webbrowser.open(self._download_url)
