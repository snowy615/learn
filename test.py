import openai
import easygui as g
import boto3
import pygame
#botocore is part of boto3
from botocore.exceptions import NoCredentialsError
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment


# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv


class Audio:

    def record_audio(self):
        # Sampling frequency
        freq = 44100

        # Recording duration
        duration = 5

        # Start recorder with the given values
        # of duration and sample frequency
        recording = sd.rec(int(duration * freq),samplerate=freq, channels=1)

        # Record audio for the given number of seconds
        sd.wait()

        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        #write("input0.wav", freq, recording)

        # Convert the NumPy array to audio file
        wv.write("input1.wav", recording, freq, sampwidth=2)


def main():
    # output_wav = "recorded_audio.wav"
    audio = Audio()
    audio.record_audio()
    


if __name__ == "__main__":
    main()