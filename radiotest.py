import os
import sys

def play_audio(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)

    try:
        if file_path.endswith('.wav'): # okay to pipe directly
            os.execvp("sudo", ["sudo", "./pi_fm_rds", "-audio", file_path])
        elif file_path.endswith('.mp3'): # need to decode first, use a sox pipe
            os.execlp("sh", "sh", "-c", f"sox -t mp3 {file_path} -t wav - | sudo ./pi_fm_rds -audio -")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
        sys.exit(1)
def main():
    play_audio("assets/bad_apple_enhanced.mp3")