import os
import sys
import subprocess
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget,
    QListWidget, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QProgressBar, QGridLayout,
    QInputDialog, QDialog, QDialogButtonBox,  # <-- add this import
)
def fetch_youtube_audio(link, output_path="."):
    # This will replace the current process with youtube-dl
    os.environ["YOUTUBE_DL_LINK"] = link
    os.environ["YOUTUBE_DL_OUTPUT_PATH"] = output_path
    cmd = 'yt-dlp -x --audio-format mp3 -o "$YOUTUBE_DL_OUTPUT_PATH/%(title)s.%(ext)s" "$YOUTUBE_DL_LINK"'
    os.execlp("sh", "sh", "-c", cmd)


# try downloading sum shi
# uhh
#fetch_youtube_audio("dQw4w9WgXcQ", "./downloads")

class YoutubeDownloadPrompt(QMainWindow):
    class CustomDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle("HELLO!")

            QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            layout = QVBoxLayout()
            filename = "unknown_file.mp3"
            try:
                filename = subprocess.check_output(["yt-dlp", "--print filename -o %(title)s.%(ext)s " + self.link + " --restrict-filenames"])
            except Exception as e:
                print(f"Error fetching filename: {e}")

            message = QLabel("Download {file} to {path}?".format(file=filename, path="./downloads"))
            layout.addWidget(message)
            layout.addWidget(self.buttonBox)
            self.setLayout(layout)
    def __init__(self):
        super().__init__()
        self.link = None
        self.output_path = None
        self.setWindowTitle("grab audio from youtube")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.link_label = QLabel("YouTube Link:")
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Enter YouTube video link here")


        self.fetch_button = QPushButton("Fetch Audio")
        self.fetch_button.clicked.connect(self.fetch_audio)

        self.layout.addWidget(self.link_label)
        self.layout.addWidget(self.link_input)

        self.layout.addWidget(self.fetch_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def fetch_audio(self):
        self.link = self.link_input.text().strip()


        if not self.link:
            print("Please enter a valid YouTube link.")
            return

        try:
            fetch_youtube_audio(self.link, "downloads")
        except Exception as e:
            print(f"Error fetching audio: {e}")

app = QApplication(sys.argv)
window = YoutubeDownloadPrompt()
window.show()
app.exec()