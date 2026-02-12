"""About tab displaying application information."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from app.constants import APP_TITLE, APP_VERSION, GITHUB_URL, AUTHOR, COPYRIGHT_YEAR


class AboutTab(QWidget):
    """Tab widget showing application metadata and credits."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addSpacing(30)

        # Application title
        lbl_title = QLabel(APP_TITLE)
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(lbl_title)

        # Version
        lbl_ver = QLabel(f"Versi {APP_VERSION}")
        lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_ver.setStyleSheet("font-size: 14px; color: #888;")
        layout.addWidget(lbl_ver)

        layout.addSpacing(20)

        # Description
        desc_text = (
            "Aplikasi desktop sederhana berbasis Python (PyQt6) "
            "untuk menampilkan jadwal sholat di berbagai kota besar di Indonesia "
            "secara real-time menggunakan API Aladhan."
        )
        lbl_desc = QLabel(desc_text)
        lbl_desc.setWordWrap(True)
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_desc.setStyleSheet("font-size: 14px; padding: 0 20px;")
        layout.addWidget(lbl_desc)

        layout.addSpacing(30)

        # Developer info
        lbl_author = QLabel("Dikembangkan oleh:")
        lbl_author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_author)

        # GitHub link (blue hardcoded for both themes)
        lbl_link = QLabel(
            f'<a href="{GITHUB_URL}" style="color: #0078d7; text-decoration: none; '
            f'font-weight: bold; font-size: 16px;">github.com/fikrisyahid</a>'
        )
        lbl_link.setOpenExternalLinks(True)
        lbl_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_link)

        # Copyright
        layout.addSpacing(20)
        lbl_copy = QLabel(f"\u00a9 {COPYRIGHT_YEAR} {AUTHOR}")
        lbl_copy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_copy.setStyleSheet("font-size: 12px; color: #888;")
        layout.addWidget(lbl_copy)

        layout.addStretch()
        self.setLayout(layout)
