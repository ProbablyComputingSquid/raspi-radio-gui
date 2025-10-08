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
    subprocess.Popen( cmd, shell=True)


# try downloading sum shi
# uhh
#fetch_youtube_audio("dQw4w9WgXcQ", "./downloads")
    class CustomDialog(QDialog):
        def __init__(self, parent=None, link=""):
            super().__init__(parent)
            self.link = link
            self.setWindowTitle("HELLO!")

            QBtn = QDialogButtonBox.StandardButton.Ok
            QBtn |= QDialogButtonBox.StandardButton.Cancel

            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            layout = QVBoxLayout()
            filename = "unknown_file.mp3"
            try:
                filename = subprocess.check_output(["yt-dlp", "--print", "filename", "-o", "%(title)s.%(ext)s", self.link, "--restrict-filenames"]).decode().strip()
            except Exception as e:
                print(f"Error fetching filename: {e}")

            message = QLabel("Download {file} to {path}?".format(file=filename, path="./downloads"))
            layout.addWidget(message)
            layout.addWidget(self.buttonBox)
            self.setLayout(layout)
class YoutubeDownloadPrompt(QDialog):

    def __init__(self):
        super().__init__()
        # load stylesheet
        with open("./assets/style.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.link = None
        self.output_path = None
        self.setWindowTitle("grab audio from youtube")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.link_label = QLabel("YouTube Link:")
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Enter YouTube video link here")


        self.fetch_button = QPushButton("Fetch Audio")

        self.query = QLabel("Google Videos Query:")
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search query here")
        self.fetch_button.clicked.connect(self.fetch_audio)

        self.layout.addWidget(self.link_label)
        self.layout.addWidget(self.link_input)

        self.layout.addWidget(self.query)
        self.layout.addWidget(self.query_input)

        self.layout.addWidget(self.fetch_button)

        self.setLayout(self.layout)

    def fetch_audio(self):
        self.link = self.link_input.text().strip()


        if not self.link:
            print("fetching audio by searching...")
            self.progress = QProgressBar()
            self.layout.addWidget(self.progress)
            self.progress.setRange(0, 0)  # Indeterminate progress
            from threading import Thread

            def run_download():
                cmd = 'yt-dlp -x --audio-format mp3 --default-search auto "' + self.query_input.text().strip() + '" -o "downloads/%(title)s.%(ext)s"'
                subprocess.run(cmd, shell=True)
                self.progress.setRange(0, 1)
                self.accept()
                self.fetch_button.setEnabled(True)


            Thread(target=run_download, daemon=True).start()
            self.fetch_button.setEnabled(False)
            return


        try:
            print("Downloading audio...")
            fetch_youtube_audio(self.link, "downloads")
            self.accept()
        except Exception as e:
            print(f"Error fetching audio: {e}")
            self.reject()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YoutubeDownloadPrompt()
    window.show()
    app.exec()