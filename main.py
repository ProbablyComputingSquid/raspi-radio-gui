import sys
import os
import random
import pygame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget,
    QListWidget, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
)

def parseSongs(files : list) -> list:
    """
    Parses a list of file paths and returns a list of song names.
    """
    songNames = []
    for file in files:
        stats = os.stat(file)  # Check if the file exists and is accessible
        print(stats)

        # fallback song name if can't fetch metadata
        # Extract the song name from the file path
        songName = file.split("/")[-1]
        # Remove the file extension
        songName = songName.split(".")[0]
        songNames.append(songName)
    return songNames

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.setWindowTitle("Raspi radio player")
        self.queue = []
        self.current_index = -1
        self.is_paused = False


        # Widgets
        # list widget to display the music queue
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        queue_header = QHBoxLayout()
        list_title = QLabel("Music Queue")
        queue_header.addWidget(list_title)
        load_btn = QPushButton("Load Music")
        queue_header.addWidget(load_btn)

        music_queue = QVBoxLayout()
        music_queue.addLayout(queue_header)
        music_queue.addWidget(self.list_widget)

        # buttons for the player controls on the bottom


        play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause/Unpause")
        skip_btn = QPushButton("Skip")
        shuffle_btn = QPushButton("Shuffle")
        remove_btn = QPushButton("Remove")

        # exit button on the top, make a layout too
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)  # Add stretch to push the content to the left
        exit_btn = QPushButton("Exit")
        top_layout.addWidget(exit_btn)

        # now playing display
        self.song_title = QLabel("Song Title") # placeholder text which will get updated
        self.song_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        song_author = QLabel("Song Author") # i hope ill figure out how to get the author later
        song_author.setStyleSheet("font-size: 14px; font-style: italic;")

        album_cover = QLabel()
        album_cover.setPixmap(QPixmap("./assets/cd_placeholder.png"))
        album_cover.setScaledContents(True)
        album_cover.setFixedSize(150, 150)
        album_cover.setStyleSheet("background-color: rgb(255, 255, 255); border: 2px solid black; padding: 10px;")
        album_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layouts
        btn_layout = QHBoxLayout()

        btn_layout.addWidget(play_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(skip_btn)
        btn_layout.addWidget(shuffle_btn)
        btn_layout.addWidget(remove_btn)

        # now playing display
        # somehow i feel like this isnt the best way to do this, but it works
        now_layout = QHBoxLayout() # holder to display the currently playing song
        song_title_layout = QVBoxLayout() # layout to stack song title and author vertically
        song_title_layout.addWidget(self.song_title)
        song_title_layout.addWidget(song_author)
        song_title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        now_layout.addWidget(album_cover)
        now_layout.addLayout(song_title_layout)

        # center block to hold the now playing display and the list widget
        center_block = QHBoxLayout()
        center_block.addLayout(music_queue)
        now_layout.addStretch(1)  # Add stretch to push the content to the left
        center_block.addLayout(now_layout)
        center_block.addStretch()
        # main layout and shi
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_block)
        main_layout.addLayout(btn_layout)

        # stick it all in a container cause yeah thats what the docs said
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # !! connect the functions to the buttons !!
        # - the play queue
        load_btn.clicked.connect(self.load_music)
        play_btn.clicked.connect(self.play_music)
        self.pause_btn.clicked.connect(self.pause_unpause_music)
        skip_btn.clicked.connect(self.skip_music)
        shuffle_btn.clicked.connect(self.shuffle_queue)
        remove_btn.clicked.connect(lambda: self.list_widget.takeItem(self.list_widget.currentRow()))
        # - the exit button
        exit_btn.clicked.connect(self.close)
        # list widget double click to play
        self.list_widget.doubleClicked.connect(self.play_selected)

    def load_music(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open Music Files", "", "Audio Files (*.mp3 *.wav)")
        if files:
            song_names = parseSongs(files)
            self.queue.extend(files)
            self.list_widget.addItems(song_names)

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
        self.pause_btn.setText("Pause")
        self.list_widget.setCurrentRow(self.current_index)
        # Update the now playing display
        song_name = self.queue[self.current_index].split("/")[-1].split(".")[0]
        self.song_title.setText(song_name)

    def pause_unpause_music(self):
        if pygame.mixer.music.get_busy():
            if self.is_paused: # so this actually never triggers if the music isnt playing
                pygame.mixer.music.unpause()
                self.pause_btn.setText("Pause")
            else:
                pygame.mixer.music.pause()
                self.pause_btn.setText("Unpause")
            self.is_paused = not self.is_paused
        else:
            print("music is not playing")
            try:
                pygame.mixer.music.unpause()
                self.pause_btn.setText("Pause")
            except pygame.error:
                print("No music is loaded to unpause.")

    def skip_music(self):
        if not self.queue:
            return
        self.current_index = (self.current_index + 1) % len(self.queue)
        self._play_current()

    def shuffle_queue(self):
        if not self.queue:
            return
        random.shuffle(self.queue)
        self.list_widget.clear()
        self.list_widget.addItems(self.queue)
        self.current_index = 0
        self._play_current()

app = QApplication(sys.argv)
window = MusicPlayer()
window.show()
app.exec()