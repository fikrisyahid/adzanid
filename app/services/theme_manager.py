"""Service for managing application themes (dark/light)."""

from PyQt6.QtWidgets import QApplication


class ThemeManager:
    """Manages the application's dark/light theme stylesheets."""

    DARK_STYLE = """
    QMainWindow, QWidget { background-color: #2b2b2b; color: #ffffff; }
    QTabWidget::pane { border: 1px solid #444; top: -1px; }
    QTabBar::tab { background: #3b3b3b; color: #fff; padding: 8px 20px; border: 1px solid #555; margin-right: 2px; }
    QTabBar::tab:selected { background: #505050; border-bottom-color: #505050; font-weight: bold; }

    QCheckBox { spacing: 5px; color: #ffffff; background: transparent; }
    QCheckBox::indicator { width: 15px; height: 15px; border: 1px solid #888; background: #3b3b3b; }
    QCheckBox::indicator:checked { background: #0078d7; border: 1px solid #0078d7; }

    QComboBox, QPushButton, QLineEdit {
        background-color: #3b3b3b; color: white; border: 1px solid #555; padding: 6px; border-radius: 4px;
    }
    QComboBox:hover, QPushButton:hover { background-color: #4a4a4a; border: 1px solid #777; }
    QComboBox::drop-down { border: 0px; }
    """

    LIGHT_STYLE = """
    QMainWindow, QWidget { background-color: #f5f5f5; color: #000000; }
    QTabWidget::pane { border: 1px solid #d0d0d0; top: -1px; background: white; }
    QTabBar::tab { background: #e0e0e0; color: #000; padding: 8px 20px; border: 1px solid #ccc; margin-right: 2px; }
    QTabBar::tab:selected { background: #ffffff; border-bottom-color: #ffffff; font-weight: bold; }

    QCheckBox { spacing: 5px; color: #000000; background: transparent; }
    QCheckBox::indicator { width: 15px; height: 15px; border: 1px solid #aaa; background: white; }
    QCheckBox::indicator:checked { background: #0078d7; border: 1px solid #0078d7; }

    QComboBox, QPushButton, QLineEdit {
        background-color: #ffffff; color: #000000; border: 1px solid #ccc; padding: 6px; border-radius: 4px;
    }
    QComboBox:hover, QPushButton:hover {
        background-color: #e6f7ff; border: 1px solid #0078d7;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff; color: #000000; selection-background-color: #0078d7; selection-color: #ffffff;
    }
    """

    def __init__(self):
        self._is_dark = False

    @property
    def is_dark(self) -> bool:
        return self._is_dark

    @is_dark.setter
    def is_dark(self, value: bool):
        self._is_dark = value

    def apply(self):
        """Apply the current theme to the application."""
        style = self.DARK_STYLE if self._is_dark else self.LIGHT_STYLE
        QApplication.instance().setStyleSheet(style)
