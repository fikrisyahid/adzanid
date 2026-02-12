"""System tray icon and menu management."""

import os

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QStyle
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import pyqtSignal, QObject

from app.constants import ICON_PATH


class SystemTrayManager(QObject):
    """Manages the system tray icon, context menu, and notifications."""

    show_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tray_icon = QSystemTrayIcon(parent)
        self._setup_icon(parent)
        self._setup_menu(parent)

        self._tray_icon.activated.connect(self._on_activated)
        self._tray_icon.messageClicked.connect(self.show_requested.emit)
        self._tray_icon.show()

    def _setup_icon(self, parent):
        """Load the tray icon from file or fall back to a system default."""
        if os.path.exists(ICON_PATH):
            icon = QIcon(ICON_PATH)
        else:
            icon = parent.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        self._tray_icon.setIcon(icon)

    def _setup_menu(self, parent):
        """Build the right-click context menu."""
        menu = QMenu()

        show_action = QAction("Tampilkan", parent)
        show_action.triggered.connect(self.show_requested.emit)

        quit_action = QAction("Keluar", parent)
        quit_action.triggered.connect(QApplication.instance().quit)

        menu.addAction(show_action)
        menu.addAction(quit_action)
        self._tray_icon.setContextMenu(menu)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_requested.emit()

    def notify(self, title: str, message: str, duration_ms: int = 5000):
        """Show a balloon notification from the tray icon."""
        self._tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            duration_ms,
        )
