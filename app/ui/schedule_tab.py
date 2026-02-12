"""Schedule tab displaying current time and prayer times."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from app.constants import PRAYER_NAMES


class ScheduleTab(QWidget):
    """Tab widget that shows the clock and today's prayer schedule."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._prayer_labels: dict[str, QLabel] = {}
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

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
