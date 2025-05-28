import os
import sys
import pygame
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.setWindowTitle("music player test")

        button = QPushButton("Play Music")
        button.pressed.connect(self.play_music)

        self.setCentralWidget(button)
        self.show()

    def play_music(self):
        pygame.mixer.music.load("music_test.mp3")
        pygame.mixer.music.play()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()