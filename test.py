import openai
import easygui as g
import boto3
import pygame
#botocore is part of boto3
from botocore.exceptions import NoCredentialsError
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

class Audio:
    def record_audio_with_threshold(output_wav, sample_rate=44100, channels=2, threshold=0.01, min_silence_duration=1):
        print("Recording...")

        audio_data = []

        def callback(indata, frames, time, status):
            if status:
                print("Error:", status)
            if any(indata > threshold):
                audio_data.extend(indata)

        # Start recording
        with sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate):
            sd.sleep(int(min_silence_duration * 1000))  # Let the recording continue for the specified silence duration

        print("Recording finished.")

        # Convert the recorded audio to WAV
        sf.write(output_wav, audio_data, sample_rate)


def main():
    output_wav = "recorded_audio.wav"
    audio = Audio()

    audio.record_audio_with_threshold(output_wav)
    


if __name__ == "__main__":
    main()