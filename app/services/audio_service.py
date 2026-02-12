"""Service for playing adhan audio files."""

import os

from PyQt6.QtCore import QUrl, QObject, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class AudioService(QObject):
    """Wraps QMediaPlayer to handle adhan audio playback."""

    playback_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        self._player.playbackStateChanged.connect(self._on_state_changed)

    def _on_state_changed(self, state: QMediaPlayer.PlaybackState):
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.playback_finished.emit()

    @property
    def is_playing(self) -> bool:
        """Return True if audio is currently playing."""
        return self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def play(self, file_path: str) -> bool:
        """Play the audio file at the given path.

        Returns:
            True if playback started, False if file not found.
        """
        if not file_path or not os.path.exists(file_path):
            return False

        self._audio_output.setVolume(1.0)
        self._player.setSource(QUrl.fromLocalFile(file_path))
        self._player.play()
        return True

    def stop(self):
        """Stop any currently playing audio."""
        self._player.stop()
