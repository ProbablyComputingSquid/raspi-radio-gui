# todo: - add icons
# todo: - add playlist support, write the current queue to a .playlist file or something, also allow loading from it
# (.playlist files are just a list of file paths, so its not that hard lmao)
import sys
import os
import random
import pygame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget,
    QListWidget, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QProgressBar, QGridLayout,
    QInputDialog, QDialog, QDialogButtonBox,  # <-- add this import
)
from mutagen.mp3 import MP3
from fetch_youtube_files import fetch_youtube_audio, YoutubeDownloadPrompt

def parse_songs(files : list) -> list:
    """
    Parses a list of file paths and returns a list of song names.
    """
    song_names = []
    for file in files:
        stats = os.stat(file)  # Check if the file exists and is accessible
        print(stats)

        # fallback song name if can't fetch metadata
        # Extract the song name from the file path
        song_name = file.split("/")[-1]
        # Remove the file extension
        song_name = " ".join(song_name.split(".")[:-1])
        song_names.append(song_name)
    return song_names
def seconds_to_time(seconds):
    """
    Converts seconds to a formatted time string (MM:SS).
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"
class AlertDialog(QDialog):
    def __init__(self, text, title = "alert!", parent=None):
            super().__init__(parent)
            self.setWindowTitle(text)
            layout = QVBoxLayout()
            layout.addWidget(QLabel(text))
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)
            self.setLayout(layout)
class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        #pygame.mixer.init(devicename="Loopback Analog Stereo")
        self.yt_dl_window = None
        pygame.mixer.init()
        self.setWindowTitle("Raspi radio player")
        self.queue = []
        self.current_index = -1
        self.is_paused = False

        self.progress_timer = QTimer(self)
        self.progress_timer.setInterval(500)  # update every 0.5 seconds
        self.progress_timer.timeout.connect(self.update_progress_bar)
        self.current_song_length = 0

        # Widgets
        # list widget to display the music queue
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        queue_header = QGridLayout()
        list_title = QLabel("Music Queue")
        load_btn = QPushButton("Load Music")
        youtube_rip_btn = QPushButton("Rip Music from Online Source")
        save_btn = QPushButton("Save Queue to Playlist")
        self.item_count = QLabel("Your queue is emptier than my soul. go add something :p")
        self.item_count.setStyleSheet("font-size: 8px; color: gray; font-style: italic;")
        queue_header.addWidget(list_title, 0, 0)
        queue_header.addWidget(load_btn, 0, 1)
        queue_header.addWidget(save_btn, 0, 2)
        queue_header.addWidget(youtube_rip_btn, 1, 0, 1, 3)
        queue_header.addWidget(self.item_count, 2, 0, 1, 3)  # row, column, row span, column span

        queue_footer = QHBoxLayout()
        play_btn = QPushButton("Play")
        remove_btn = QPushButton("Remove Track")
        queue_footer.addWidget(play_btn)
        queue_footer.addWidget(remove_btn)
        music_queue = QVBoxLayout()
        music_queue.addLayout(queue_header)
        music_queue.addWidget(self.list_widget)
        music_queue.addLayout(queue_footer)

        # buttons for the player controls on the bottom


        self.pause_btn = QPushButton("▶")
        previous_btn = QPushButton("⏮")
        skip_btn = QPushButton("⏭") # not sure if i should use an icon or text, but we copying spotify
        shuffle_btn = QPushButton("🔀") # i absolutely hate this emoji, i want unicode


        # exit button on the top, make a layout too
        top_layout = QHBoxLayout()
        self.title_label = QLabel("Raspi Radio Player")
        top_layout.addWidget(self.title_label)
        top_layout.addStretch(1)  # Add stretch to push the content to the left
        exit_btn = QPushButton("Exit")
        top_layout.addWidget(exit_btn)

        # now playing display
        self.song_title = QLabel("Song Title") # placeholder text which will get updated
        self.song_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        song_author = QLabel("Song Author") # i hope ill figure out how to get the author later
        song_author.setStyleSheet("font-size: 14px; font-style: italic;")
        self.song_progress = QProgressBar()
        self.song_progress.setRange(0, 100)
        self.song_progress.setTextVisible(False)
        self.song_progress.setMinimumWidth(400)  # Make the progress bar wider
        self.song_progress_label = QLabel("--:-- / --:--")  # Placeholder for time display
        self.song_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.song_progress_label.setStyleSheet("font-size: 12px; color: orangered; border: 0px;")

        album_cover = QLabel()
        album_cover.setPixmap(QPixmap("./assets/cd_placeholder.png"))
        album_cover.setScaledContents(True)
        album_cover.setFixedSize(150, 150)
        album_cover.setStyleSheet("background-color: darkgray; border: 2px solid orangered; padding: 10px;")
        album_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # button layout under songs
        btn_layout = QHBoxLayout()
#        btn_layout.addWidget(play_btn)
        btn_layout.addWidget(previous_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(skip_btn)
        btn_layout.addWidget(shuffle_btn)
        #btn_layout.addWidget(remove_btn)

        # now playing display
        # somehow i feel like this isnt the best way to do this, but it works
        now_layout = QHBoxLayout() # holder to display the currently playing song
        song_title_layout = QVBoxLayout() # layout to stack song title and author vertically
        song_title_layout.addWidget(self.song_title)
        song_title_layout.addWidget(song_author)
        song_title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        song_title_layout.addWidget(self.song_progress)
        song_title_layout.addWidget(self.song_progress_label)
        song_title_layout.addLayout(btn_layout)
        now_layout.addWidget(album_cover)
        now_layout.addLayout(song_title_layout)
        now_playing_layout = QVBoxLayout()
        now_playing_layout.addLayout(now_layout)

        # center block to hold the now playing display and the list widget
        center_block = QHBoxLayout()
        center_block.addLayout(music_queue)

        center_block.addStretch()  # Add stretch to push the content to the left
        center_block.addLayout(now_playing_layout)
        center_block.addStretch()
        # main layout and shi
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_block)


        # stick it all in a container cause yeah thats what the docs said
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # !! connect the functions to the buttons !!
        # - the play queue
        load_btn.clicked.connect(self.load_music)
        save_btn.clicked.connect(self.prompt_and_save_playlist)
        play_btn.clicked.connect(self.play_music)
        self.pause_btn.clicked.connect(self.pause_unpause_music)
        previous_btn.clicked.connect(self.previous_music)
        skip_btn.clicked.connect(self.skip_music)
        shuffle_btn.clicked.connect(self.shuffle_queue)
        remove_btn.clicked.connect(self.removeTrack)
        youtube_rip_btn.clicked.connect(self.rip_music) # im an actual idiot, i forgot to connect it and was straight up tweaking
        # - the exit button
        exit_btn.clicked.connect(self.close)
        # list widget double click to play
        self.list_widget.doubleClicked.connect(self.play_selected)

        # load stylesheet
        # with whatever the fuck qss is, i guess we have our own language now
        with open("./assets/style.qss", "r") as f:
            self.setStyleSheet(f.read())
    # todo: remove track doesnt actually remove from self.queue
    def removeTrack(self): # removes current track
        self.queue.pop(self.list_widget.currentRow())
        self.list_widget.takeItem(self.list_widget.currentRow())
        self.item_count.setText(f"There are {len(self.queue)} tracks in queue")
        self._play_current()
    # extends the queue with a selected file name
    def load_music_file(self, path: str):
        song_names = parse_songs([path])
        self.queue.extend([path])
        self.list_widget.addItems(song_names)
        self.item_count.setText(f"There are {len(self.queue)} tracks in queue")
    def load_music(self):
        files, _filter = QFileDialog.getOpenFileNames(self, "Open Music Files", "/home", "Audio Files (*.mp3 *.wav);;Playlists (*.playlist)")
        if files:
            if _filter == "Playlists (*.playlist)":
                title, files = self.load_playlist(files)
            song_names = parse_songs(files)
            self.queue.extend(files)
            self.list_widget.addItems(song_names)
            self.item_count.setText(f"There are {len(self.queue)} tracks in queue")
    def load_playlist(self, playlist_path):
        info = ""
        if isinstance(playlist_path, list): # only allow one playlist at a time. not sure why you would want to load multiple playlists at once
            playlist_path = playlist_path[0]
        with open(playlist_path, "r") as f:
            info = f.read().splitlines()
        if not info:
            return None # nothing in the file
        title = info[0] # first line is the title
        if not title:
            title = "Untitled Playlist"
        self.title_label.setText("Raspi Radio Gui - " + title)  # update the title label
        return title, info[1:]  # rest of the lines are the file paths

    def prompt_and_save_playlist(self):
        title, ok = QInputDialog.getText(self, "Playlist Name", "Enter a name for your playlist:")
        if ok and title:
            self.save_playlist(title)

    def save_playlist(self, title):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Playlist", "", "Playlists (*.playlist)")
        if not filename:
            return None
        with open(filename, "w") as f:
            f.write(title + "\n")
            for song in self.queue:
                f.write(song + "\n")
        return filename

    def play_music(self):
        if not self.queue:
            return
        if self.current_index == -1:
            self.current_index = 0
        self._play_current()

    def play_selected(self, index):
        self.current_index = index.row()
        self._play_current()

    def _play_current(self):

        pygame.mixer.music.load(self.queue[self.current_index])
        pygame.mixer.music.play()
        self.is_paused = False
        self.pause_btn.setText("⏸")
        self.list_widget.setCurrentRow(self.current_index)
        # Update the now playing display
        song_name = self.queue[self.current_index].split("/")[-1].split(".")[0]
        self.song_title.setText(song_name)

        # Get song length (in seconds)
        try:
            self.current_song_length = self.get_song_length(self.queue[self.current_index])
            self.song_progress.setRange(0, int(self.current_song_length * 1000))  # use ms for more granularity
        except Exception as e:
            self.current_song_length = 0
            self.song_progress.setRange(0, 100)
        self.song_progress.setValue(0)
        self.progress_timer.start()
        self.song_progress_label.setText(f"00:00 / {seconds_to_time(int(self.current_song_length))}")
    # update the progress bar every 0.5 seconds or so
    def update_progress_bar(self):
        if (len(self.queue)) == 0: # just stick this here to auto update, its bad practice i knowww
            self.queue.extend("Load some music first ^w^")
        if pygame.mixer.music.get_busy() and self.current_song_length > 0 and not self.is_paused:
            pos_ms = pygame.mixer.music.get_pos()  # ms since music started playing
            # Clamp to song length
            if pos_ms > self.current_song_length * 1000:
                pos_ms = self.current_song_length * 1000
            self.song_progress.setValue(pos_ms)
            self.song_progress_label.setText(f"{seconds_to_time(pos_ms // 1000)} / {seconds_to_time(int(self.current_song_length))}")
        elif not pygame.mixer.music.get_busy():
            self.song_progress.setValue(self.song_progress.maximum())
            self.progress_timer.stop()

    def get_song_length(self, filepath):
        # Use pygame's Sound for wav, or mutagen for mp3
        if filepath.lower().endswith('.wav'):
            sound = pygame.mixer.Sound(filepath)
            return sound.get_length()
        elif filepath.lower().endswith('.mp3'):
            try:
                audio = MP3(filepath)
                return audio.info.length
            except Exception as e:
                print("an error hath occurred:" + str(e))
                return 0
        else:
            return 0

    def pause_unpause_music(self):
        if pygame.mixer.music.get_busy():
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.pause_btn.setText("⏸")
                self.progress_timer.start()
            else:
                pygame.mixer.music.pause()
                self.pause_btn.setText("▶")
                self.progress_timer.stop()
            self.is_paused = not self.is_paused
        else:
            print("music is not playing")
            try:
                pygame.mixer.music.unpause()
                self.pause_btn.setText("⏸")
                self.progress_timer.start()
            except pygame.error:
                print("No music is loaded to unpause.")

    def skip_music(self):
        if not self.queue:
            return
        self.current_index = (self.current_index + 1) % len(self.queue)
        self._play_current()
    def previous_music(self):
        if not self.queue:
            return
        self.current_index = (self.current_index - 1) % len(self.queue)
        self._play_current()
    def shuffle_queue(self):
        if not self.queue:
            return
        random.shuffle(self.queue)
        self.list_widget.clear()
        self.list_widget.addItems(parse_songs(self.queue))
        self.current_index = 0
        self._play_current()

    # pull music from youtube or other source
    def rip_music(self):
        print("here!")
        self.yt_dl_window = YoutubeDownloadPrompt()
        self.yt_dl_window.setModal(True)
        result = self.yt_dl_window.open()

        if result == QDialog.accepted:
            final_destination = self.yt_dl_window.output_path
            download_alert = AlertDialog("successfully downloaded to " + final_destination, "Downloading...", self)
            download_alert.show()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()

    app.exec()