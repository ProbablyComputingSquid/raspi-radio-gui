# todo: - add icons
# todo: - add playlist support, write the current queue to a .playlist file or something, also allow loading from it
# (.playlist files are just a list of file paths, so its not that hard lmao)
import sys
import os
import random
import subprocess
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QMetaObject
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget,
    QListWidget, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QProgressBar, QGridLayout,
    QInputDialog, QDialog, QDialogButtonBox, QComboBox
)
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen import File
from mutagen.id3 import ID3, APIC
from threading import Thread
from pydub import AudioSegment
import simpleaudio as sa





class YoutubeDownloadPrompt(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        # load stylesheet
        self.progress = None
        with open("./assets/style.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.link = None
        self.output_path = None
        self.loading_label = QLabel()
        self.setWindowTitle("grab audio from youtube")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.link_label = QLabel("Link to a website (youtube, soundcloud, etc.) with a music file and we will attempt to extract the audio for you. We can download playlists too!:")
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Enter website link here, e.g. ")

        self.site_combobox = QComboBox()
        with open("./assets/supported_sites.txt", "r") as f:
            sites = f.read().splitlines()
        self.site_combobox.setEditable(True)
        self.site_combobox.addItem("auto")
        self.site_combobox.addItems(sites)
        self.combo_label = QLabel("look through this list of supported sites to see if your site is supported, otherwise leave it as 'auto':")
        self.combo_label.setWordWrap(True)
        self.fetch_button = QPushButton("Fetch Audio")

        self.query = QLabel("Extract song from youtube by searching (if no link is provided).")
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search query here")

        self.fetch_button.setToolTip("Click to fetch audio from the provided link or search query.")

        self.fetch_button.clicked.connect(self.fetch_audio)

        self.downloaded_file = None  # Store the downloaded filename

        self.layout.addWidget(self.link_label)
        self.layout.addWidget(self.link_input)
        self.layout.addWidget(self.combo_label)
        self.layout.addWidget(self.site_combobox)
        self.layout.addWidget(self.query)
        self.layout.addWidget(self.query_input)

        self.layout.addWidget(self.fetch_button)
        self.layout.addWidget(self.loading_label)

        self.setLayout(self.layout)

    @QtCore.pyqtSlot()
    def finish_download(self):
        self.progress.setRange(0, 1)
        self.fetch_button.setEnabled(True)
        self.progress.deleteLater()
        self.accept()  # Close the window

    def fetch_audio(self):
        self.link = self.link_input.text().strip()
        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)
        self.progress.setRange(0, 0)  # Indeterminate progress
        if not self.link:
            print("fetching audio by searching...")


            site = self.site_combobox.currentText().strip()
            query = self.query_input.text().strip()
            # Get the expected filename before download
            def get_filename():
                filename = subprocess.check_output([
                "yt-dlp", "--print", "filename", "--default-search", site,
                "-o", "downloads/%(title)s.mp3", query, "--restrict-filenames"
                ]).decode().strip()
                self.downloaded_file = filename
            QMetaObject.invokeMethod(self, "get_filename", Qt.ConnectionType.QueuedConnection)
            def run_download():
                cmd = (
                    'yt-dlp -x --audio-format mp3 --default-search ' + site +
                    ' "' + query +
                    '" -o "downloads/%(title)s.%(ext)s" --embed-thumbnail --embed-metadata --restrict-filenames --write-thumbnail'
                )
                subprocess.run(cmd, shell=True)
                QMetaObject.invokeMethod(self, "finish_download", Qt.ConnectionType.QueuedConnection)

            Thread(target=run_download, daemon=True).start()
            self.fetch_button.setEnabled(False)

            return

        try:
            print("Downloading audio...")

            # Get the expected filename before download
            def obtain_filename():
                filename = subprocess.check_output([
                "yt-dlp", "--print", "filename", "-o", "downloads/%(title)s.mp3", self.link, "--restrict-filenames"
                ]).decode().strip()
                self.downloaded_file = filename
            QMetaObject.invokeMethod(self, "obtain_filename", Qt.ConnectionType.QueuedConnection)
            def run_download():
                cmd = (
                    'yt-dlp -x --audio-format mp3 "' + self.link +
                    '" -o "downloads/%(title)s.%(ext)s"' +
                    '--embed-thumbnail --embed-metadata --restrict-filenames --write-thumbnail'
                )
                subprocess.run(cmd, shell=True)
                QMetaObject.invokeMethod(self, "finish_download", Qt.ConnectionType.QueuedConnection)

            Thread(target=run_download, daemon=True).start()
            self.fetch_button.setEnabled(False)

            return
        except Exception as e:
            print(f"Error fetching audio: {e}")
            self.reject()



def parse_songs(files : list) -> list:
    """
    Parses a list of file paths and returns a list of song names.
    """
    song_names = []
    for file in files:
        print("parsing file: " + file)
        stats = os.stat(file)  # Check if the file exists and is accessible
        print(stats)

        # fallback song name if can't fetch metadata
        # Extract the song name from the file path
        song_name = os.path.basename(file)
        # Remove the file extension
        song_name = " ".join(song_name.split(".")[:-1])
        song_names.append(song_name)
    return song_names
def seconds_to_time(seconds):
    """
    Converts seconds to a formatted time string (MM:SS).
    """
    minutes = int(seconds) // 60
    seconds = int(seconds) % 60
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
        # load stylesheet
        # with whatever the fuck qss is, i guess we have our own language now
        with open("./assets/style.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.yt_dl_window = None
        self.setWindowTitle("Raspi radio player")
        self.queue = []
        self.current_index = -1
        self.is_paused = False
        self.is_playing = False
        self.current_song_length = 0
        self.current_audio = None
        self.current_play_obj = None
        self.current_audio_pos = 0  # in ms
        self.progress_timer = QTimer(self)
        self.progress_timer.setInterval(500)  # update every 0.5 seconds
        self.progress_timer.timeout.connect(self.update_progress_bar)

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
        self.shuffle_btn = QPushButton()
        shuffle_icon = QIcon("./assets/shuffle_red.png")
        self.shuffle_btn.setIcon(shuffle_icon)
        self.shuffle_btn.setIconSize(QtCore.QSize(24, 24))

        # dont question why im doing this jank
        btn_styles = """
            padding: 2vh;
            border: 0px !important;
        """
        self.pause_btn.setStyleSheet("font-size: 24px;" + btn_styles) # make the pause button bigger
        previous_btn.setStyleSheet("font-size: 18px;" + btn_styles)
        skip_btn.setStyleSheet("font-size: 18px;" + btn_styles)
        self.shuffle_btn.setStyleSheet("font-size: 18px;" + btn_styles)

        # exit button on the top, make a layout too
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)  # Add stretch to push the content to the left
        exit_btn = QPushButton("Exit")
        top_layout.addWidget(exit_btn)

        # now playing display
        self.song_title = QLabel("Song Title") # placeholder text which will get updated
        self.song_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.song_author = QLabel("Song Author") # i hope ill figure out how to get the author later
        self.song_author.setStyleSheet("font-size: 14px; font-style: italic;")
        self.song_progress = QProgressBar()
        self.song_progress.setRange(0, 100)
        self.song_progress.setTextVisible(False)
        self.song_progress.setMinimumWidth(400)  # Make the progress bar wider

        self.song_progress_label = QLabel("--:-- / --:--")  # Placeholder for time display
        self.song_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.song_progress_label.setStyleSheet("font-size: 12px; color: orangered; border: 0px;")

        # todo: fix the stretch on the album cover
        self.album_cover = QLabel()
        self.album_cover.setPixmap(QPixmap("./assets/cd_placeholder.png"))
        self.album_cover.setScaledContents(True)
        self.album_cover.setMinimumWidth(150)
        self.album_cover.setFixedHeight(150)
        self.album_cover.setStyleSheet("background-color: darkgray; border: 2px solid orangered; border-radius: 7px;")
        self.album_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # button layout under songs
        btn_layout = QHBoxLayout()

        btn_layout.addWidget(previous_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(skip_btn)
        btn_layout.addWidget(self.shuffle_btn)


        # now playing display
        # somehow i feel like this isnt the best way to do this, but it works
        now_layout = QHBoxLayout() # holder to display the currently playing song

        song_title_layout = QVBoxLayout() # layout to stack song title and author vertically
        song_title_layout.addWidget(self.song_title)
        song_title_layout.addWidget(self.song_author)
        song_title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        song_title_layout.addWidget(self.song_progress)
        song_title_layout.addWidget(self.song_progress_label)
        song_title_layout.addLayout(btn_layout)
        now_layout.addWidget(self.album_cover)
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
        self.shuffle_btn.clicked.connect(self.shuffle_queue)
        remove_btn.clicked.connect(self.removeTrack)
        youtube_rip_btn.clicked.connect(self.rip_music) # im an actual idiot, i forgot to connect it and was straight up tweaking
        # - the exit button
        exit_btn.clicked.connect(self.close)
        # list widget double click to play
        self.list_widget.doubleClicked.connect(self.play_selected)


    # todo: remove track doesnt actually remove from self.queue
    def removeTrack(self): # removes current track
        self.queue.pop(self.list_widget.currentRow())
        self.list_widget.takeItem(self.list_widget.currentRow())
        self.item_count.setText(f"There are {len(self.queue)} tracks in queue")
        if len(self.queue) > 0:
            self._play_current()
    # extends the queue with a selected file name
    def load_music_file(self, path: str):
        print("attempting to load file: " + path)
        path_list = [path, " "]
        path_list.pop(1)

        song_names = parse_songs(path_list)
        self.queue.extend(path_list)
        self.list_widget.addItems(song_names)
        self.item_count.setText(f"There are {len(self.queue)} tracks in queue")
    def load_music(self):
        files, _filter = QFileDialog.getOpenFileNames(self, "Open Music Files", "/home", "Audio Files (*.mp3 *.wav);;Playlists (*.playlist)")
        if files:
            if _filter == "Playlists (*.playlist)":
                title, files = self.load_playlist(files)
            song_names = parse_songs(files)
            if len(self.queue) == 1 and self.queue[0] == "Load some music first ^w^":
                self.queue = []
            self.queue.extend(files)
            if len(self.queue) == len(files):
                self.play_music()
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
        if self.current_index <= -1:
            self.current_index = 0
        self._play_current()

    def play_selected(self, index):
        self.current_index = index.row()
        self._play_current()

    def _play_current(self):

        if self.current_index < 0 or self.current_index >= len(self.queue):
            return
        self.is_paused = False
        self.is_playing = True
        self.pause_btn.setText("⏸")
        self.list_widget.setCurrentRow(self.current_index)
        song_name = self.queue[self.current_index].split("/")[-1].split(".")[0]
        #self.song_title.setText(song_name)

        # Extract and display album art thumbnail
        album_pixmap = QPixmap("./assets/cd_placeholder.png")
        filepath = self.queue[self.current_index]
        if filepath.lower().endswith('.mp3'):
            try:
                tags = ID3(filepath)
                for tag in tags.values():
                    if isinstance(tag, APIC):
                        img_data = tag.data
                        pixmap = QPixmap()
                        pixmap.loadFromData(img_data)
                        if not pixmap.isNull():
                            album_pixmap = pixmap
                        break
            except Exception as e:
                print(f"Error extracting album art: {e}")
            try:
                audio = EasyID3(filepath)
                artist = audio.get('artist', ['Unknown Artist'])[0]
                title = audio.get('title', [song_name])[0]
                self.song_author.setText(artist)
                self.song_title.setText(title)
            except Exception as e:
                print(f"Error extracting metadata: {e}")
                self.song_author.setText("Unknown Artist")
                self.song_title.setText(song_name)
        self.album_cover.setPixmap(album_pixmap)
        self.album_cover.setScaledContents(True)
        ## if announcement

        # Stop previous playback if any
        if self.current_play_obj:
            self.current_play_obj.stop()
            self.current_play_obj = None
        self.current_audio_pos = 0

        filepath = self.queue[self.current_index]
        # Load audio
        try:
            self.current_audio = AudioSegment.from_file(filepath)
            self.current_song_length = self.current_audio.duration_seconds
        except Exception as e:
            print(f"Error loading audio: {e}")
            self.current_audio = None
            self.current_song_length = 0
            return

        # Play audio
        def play_audio(start_ms):
            segment = self.current_audio[start_ms:]
            self.current_play_obj = sa.play_buffer(
                segment.raw_data,
                num_channels=segment.channels,
                bytes_per_sample=segment.sample_width,
                sample_rate=segment.frame_rate
            )
            self.current_play_obj.wait_done()
            self.is_playing = False
            self.skip_music()

        self.audio_thread = Thread(target=play_audio, args=(self.current_audio_pos,), daemon=True)
        self.audio_thread.start()

        self.song_progress.setRange(0, int(self.current_song_length * 1000))  # use ms for more granularity
        self.song_progress.setValue(0)
        self.progress_timer.start()
        self.song_progress_label.setText(f"00:00 / {seconds_to_time(int(self.current_song_length))}")
    # update the progress bar every 0.5 seconds or so
    def update_progress_bar(self):
        if not self.current_audio or not self.is_playing:
            self.song_progress.setValue(self.song_progress.maximum())
            self.progress_timer.stop()
            return
        # Estimate position
        if self.current_play_obj and self.current_play_obj.is_playing():
            self.current_audio_pos += self.progress_timer.interval()
            if self.current_audio_pos > self.current_song_length * 1000:
                self.current_audio_pos = self.current_song_length * 1000
            self.song_progress.setValue(self.current_audio_pos)
            self.song_progress_label.setText(f"{seconds_to_time(self.current_audio_pos // 1000)} / {seconds_to_time(int(self.current_song_length))}")
        else:
            self.song_progress.setValue(self.song_progress.maximum())
            self.progress_timer.stop()
            if self.is_playing:
                self.skip_music()

    def pause_unpause_music(self):
        if not self.current_audio or not self.current_play_obj:
            return
        if self.is_paused:
            # Unpause: play from where left off
            self.is_paused = False
            self.pause_btn.setText("⏸")
            self.progress_timer.start()
            def play_audio(start_ms):
                segment = self.current_audio[start_ms:]
                self.current_play_obj = sa.play_buffer(
                    segment.raw_data,
                    num_channels=segment.channels,
                    bytes_per_sample=segment.sample_width,
                    sample_rate=segment.frame_rate
                )
                self.current_play_obj.wait_done()
                self.is_playing = False
                self.skip_music()
            self.audio_thread = Thread(target=play_audio, args=(self.current_audio_pos,), daemon=True)
            self.audio_thread.start()
        else:
            # Pause: stop playback and record position
            if self.current_play_obj.is_playing():
                self.current_play_obj.stop()
            self.is_paused = True
            self.pause_btn.setText("▶")
            self.progress_timer.stop()

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
        shuffle_icon = QIcon("./assets/shuffle_orange.png")
        self.shuffle_btn.setIcon(shuffle_icon)
        if not self.queue:
            return
        random.shuffle(self.queue)
        self.list_widget.clear()
        self.list_widget.addItems(parse_songs(self.queue))
        #self.current_index = 0
        #self._play_current()

    # pull music from youtube or other source
    def rip_music(self):
        print("here!")
        self.yt_dl_window = YoutubeDownloadPrompt(self)
        self.yt_dl_window.setModal(True)
        result = self.yt_dl_window.exec()
        print("result: " + str(result))
        if result == 1: # accepted
            downloaded_file = os.path.abspath(self.yt_dl_window.downloaded_file)
            print("success!" + downloaded_file)
            if downloaded_file and os.path.exists(downloaded_file):
                download_alert = AlertDialog("successfully downloaded to " + downloaded_file, "Downloading...", self)
                download_alert.exec()
                self.load_music_file(downloaded_file)
                self.play_music()
            else:
                download_alert = AlertDialog("Download finished, but file not found.", "Downloading...", self)
                download_alert.exec()
        pass

def get_song_metadata(filepath):
    """
    Returns a dictionary of metadata for the given song file.
    Supports MP3 and most common formats.
    """
    song_metadata = {}
    try:
        audio = File(filepath, easy=True)
        if audio is not None:
            for key in audio.keys():
                song_metadata[key] = audio.get(key, [""])[0]
    except Exception as e:
        print(f"Error reading metadata: {e}")
    return song_metadata


#metadata = get_song_metadata("【東方】Bad Apple!! ＰＶ【影絵】 [FtutLA63Cp8].mp3")
#print(metadata)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()

    app.exec()
