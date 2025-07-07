import sys
import os
import random
import pygame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from radiotest import play_audio # radio playing function i think works??
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget,
    QListWidget, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QProgressBar, QGridLayout,
    QInputDialog,  # <-- add this import
)
class TransmitRadio(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.setWindowTitle("Raspi Radio Player - Adjust Transmission")
        with open("./assets/style.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.setGeometry(100, 100, 800, 600)

        # list of parameters
        self.parameters = {
            "Frequency": 100.0,  # in MHz
            "Volume": 50,  # in percentage
            "Audio File": "",
        }

        # okay so hear me out
        # a vertical layout is a stack
        # and a horizontal layout is a burger
        # wait
        # no it would be like a hotdog
        # or horizontal sandwhich
        # wait this doesnt make any sense at all
        # im still calling it a burger

        # layout stack with parameter inputs
        # burger for frequency input
        self.frequency_burger = QHBoxLayout()
        self.frequency_input = QLineEdit()
        self.frequency_input.setPlaceholderText("Frequency (MHz)")
        self.frequency_input_label = QLabel("Frequency:")
        self.frequency_burger.addWidget(self.frequency_input_label)
        self.frequency_burger.addWidget(self.frequency_input)
        # volume burger
        # big burger is louder than small burger
        # what am i saying i think its the fever talking
        self.volume_burger = QHBoxLayout()
        self.volume_input = QLineEdit()
        self.volume_input.setPlaceholderText("Volume (%)")
        self.volume_input_label = QLabel("Volume:")
        self.volume_burger.addWidget(self.volume_input_label)
        self.volume_burger.addWidget(self.volume_input)

        self.stack_of_burgers = QVBoxLayout()
        self.stack_of_burgers.addLayout(self.frequency_burger)
        self.stack_of_burgers.addLayout(self.volume_burger)

        self.transmit_button = QPushButton("Begin Transmission")


        self.central_stack = QVBoxLayout()
        self.central_stack.addLayout(self.stack_of_burgers)
        self.central_stack.addStretch(1)
        self.central_stack.addWidget(self.transmit_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_stack)
        self.setCentralWidget(self.central_widget)


def transmit():

app = QApplication(sys.argv)
window = TransmitRadio()
window.show()
app.exec()