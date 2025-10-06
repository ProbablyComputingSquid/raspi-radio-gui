import os
import sys

def play_audio_with_sox_and_pifm():
    # This will replace the current process with the shell pipeline
    cmd = "sox -t mp3 bad_apple_enhanced.mp3 -t wav - | sudo ./pi_fm_rds -audio -"
    os.execlp("sh", "sh", "-c", cmd)

def main():
    play_audio_with_sox_and_pifm()

