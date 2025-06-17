import sys
import random
import pygame
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget,
    QListWidget, QFileDialog, QHBoxLayout
)

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.setWindowTitle("Raspi radio player")
        self.queue = []
        self.current_index = -1
        self.is_paused = False


        # Widgets
        self.list_widget = QListWidget()
        load_btn = QPushButton("Load Music")
        play_btn = QPushButton("Play")
        pause_btn = QPushButton("Pause/Unpause")
        skip_btn = QPushButton("Skip")
        shuffle_btn = QPushButton("Shuffle")
        remove_btn = QPushButton("Remove")
        exit_btn = QPushButton("Exit")

        # Layouts
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(load_btn)
        btn_layout.addWidget(play_btn)
        btn_layout.addWidget(pause_btn)
        btn_layout.addWidget(skip_btn)
        btn_layout.addWidget(shuffle_btn)
        btn_layout.addWidget(remove_btn)

        top_layout = QHBoxLayout()
        top_layout.addWidget(exit_btn)


        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(btn_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connections
        load_btn.clicked.connect(self.load_music)
        play_btn.clicked.connect(self.play_music)
        pause_btn.clicked.connect(self.pause_unpause_music)
        skip_btn.clicked.connect(self.skip_music)
        shuffle_btn.clicked.connect(self.shuffle_queue)
        remove_btn.clicked.connect(lambda: self.list_widget.takeItem(self.list_widget.currentRow()))

        self.list_widget.doubleClicked.connect(self.play_selected)

    def load_music(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open Music Files", "", "Audio Files (*.mp3 *.wav)")
        if files:
            self.queue.extend(files)
            self.list_widget.addItems(files)

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
        self.list_widget.setCurrentRow(self.current_index)

    def pause_unpause_music(self):
        if pygame.mixer.music.get_busy():
            if self.is_paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            self.is_paused = not self.is_paused

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