# okay so this is going to be an interesting one, people will load their vocaloids
# and then the file will turn them into a wav file from text which will then be played on the radio station

from g2p_en import G2p
import os
import whisper
from pydub import AudioSegment
import nltk
# Ensure that the necessary NLTK resources are downloaded
nltk.download('averaged_perceptron_tagger_eng')

g2p = G2p()

"""record phonemes from an audio file using whisper and g2p_en"""

def record_phonemes_from_file(audio_file_path, transcript_output_path=None):
    print("Loading whisper model...")
    model = whisper.load_model("base")
    print("Model loaded successfully. (I hope)")
    result = model.transcribe(audio_file_path)
    transcript = result['text']
    print("Transcription complete:" + transcript)
    if transcript_output_path:
        with open(transcript_output_path, 'w') as f:
            f.write(transcript)
        print(f"Transcript saved to {transcript_output_path}")
    phonemes_recorded = g2p(transcript)
    print(phonemes_recorded)


"""
shitty hack job of a vocaloid system thats just like a text to speech system except you use your voice. takes a lot of work to set up, but its simple to use"""
def text_phonemes_tts(text, phonemes_folder_path, output_file_format = "wav",):
    supported_formats = ["wav", "ogg", "mp3", "raw"]
    output = AudioSegment.silent(duration=0)
    phonemes = g2p(text)
    for phoneme in phonemes:
        phoneme_file = os.path.join(phonemes_folder_path, f"{phoneme}.wav")
        if os.path.exists(phoneme_file):
            phoneme_audio = AudioSegment.from_wav(phoneme_file)
            output += phoneme_audio
        else:
            print(f"Warning: Phoneme file {phoneme_file} does not exist. Skipping.")
    if not output_file_format in supported_formats:
        raise ValueError(f"Unsupported output file format. Please use one of: {", ".join(supported_formats)}.")
    output.export(f"output.{output_file_format}", format=output_file_format)

def test_g2p():
    text = "Hello, this is a test of the G2P system."
    phonemes = g2p(text)
    print(f"Text: {text}")
    print(f"Phonemes: {phonemes}")
test_g2p()
record_phonemes_from_file("vocoder_data/test_vocoder.mp3", "vocoder_data/test_vocoder_transcript.txt")

import montreal_forced_aligner
# montreal forced alignment

def test_mfa(file_path):
    # try doing mfa on an example audio file
    try:

        #os.execvp("sh", ["sh", "mfa.sh"])
        print("MFA alignment completed successfully.")
    except ImportError:
        print("Montreal Forced Aligner is not installed. Please install it to use this feature.")
    except Exception as e:
        print(f"An error occurred during MFA alignment: {e}")
    pass
test_mfa("vocoder_data/test_vocoder.mp3")
