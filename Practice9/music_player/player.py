import pygame
import os


class MusicPlayer:
    """
    Music player that manages a playlist and handles
    play/stop/next/previous track operations.
    """

    def __init__(self, music_folder="music"):
        pygame.mixer.init()
        self.music_folder = music_folder
        self.playlist = []          # List of track file paths
        self.current_index = 0      # Index of the currently loaded track
        self.is_playing = False     # Playback state

        self._load_playlist()

    def _load_playlist(self):
        """Scan music folder and load all .mp3 and .wav files."""
        supported = (".mp3", ".wav", ".ogg")
        if os.path.exists(self.music_folder):
            for filename in sorted(os.listdir(self.music_folder)):
                if filename.lower().endswith(supported):
                    self.playlist.append(os.path.join(self.music_folder, filename))

    def get_track_name(self):
        """Return the name of the current track (without path/extension)."""
        if not self.playlist:
            return "No tracks found"
        filename = os.path.basename(self.playlist[self.current_index])
        return os.path.splitext(filename)[0]

    def get_status(self):
        """Return current playback status string."""
        if not self.playlist:
            return "No tracks loaded"
        return "Playing" if self.is_playing else "Stopped"

    def get_position(self):
        """Return playback position in seconds (approximate)."""
        if self.is_playing:
            return pygame.mixer.music.get_pos() // 1000  # ms -> seconds
        return 0

    def play(self):
        """Play (or resume) the current track."""
        if not self.playlist:
            return
        if not self.is_playing:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True

    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        """Advance to the next track in the playlist."""
        if not self.playlist:
            return
        self.stop()
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        """Go back to the previous track in the playlist."""
        if not self.playlist:
            return
        self.stop()
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def track_count(self):
        """Return total number of tracks in the playlist."""
        return len(self.playlist)
