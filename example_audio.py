import boto3

# Create a Polly client
polly = boto3.client("polly")

# Text to be converted to speech
text = "Hello, this is a text-to-speech example using AWS Polly."

try:
    # Request speech synthesis
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna"
    )
    
    # Access the audio stream from the response
    audio_stream = response["AudioStream"].read()

    # Save the audio stream to a file
    with open("output.mp3", "wb") as file:
        file.write(audio_stream)

    print("Speech synthesis successful. Audio saved as 'output.mp3'")
except Exception as e:
    print("Error:", e)
