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
        self._volume: float = 1.0
        self._muted: bool = False

    def _on_state_changed(self, state: QMediaPlayer.PlaybackState):
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.playback_finished.emit()

    @property
    def is_playing(self) -> bool:
        """Return True if audio is currently playing."""
        return self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    @property
    def volume(self) -> float:
        """Return the current volume level (0.0 to 1.0)."""
        return self._volume

    @volume.setter
    def volume(self, value: float):
        """Set the volume level (0.0 to 1.0)."""
        self._volume = max(0.0, min(1.0, value))
        self._audio_output.setVolume(self._volume)

    @property
    def muted(self) -> bool:
        """Return True if audio is muted."""
        return self._muted

    @muted.setter
    def muted(self, value: bool):
        """Set the mute state."""
        self._muted = value
        self._audio_output.setMuted(value)

    def play(self, file_path: str) -> bool:
        """Play the audio file at the given path.

        Returns:
            True if playback started, False if file not found or muted.
        """
        if self._muted:
            return False

        if not file_path or not os.path.exists(file_path):
            return False

        self._audio_output.setVolume(self._volume)
        self._player.setSource(QUrl.fromLocalFile(file_path))
        self._player.play()
        return True

    def stop(self):
        """Stop any currently playing audio."""
        self._player.stop()
