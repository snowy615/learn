
import openai
import easygui as g
import boto3
import pygame
#botocore is part of boto3
from botocore.exceptions import NoCredentialsError
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

#------------------------------------------------------------------------------------------------------------------------------------

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



    def audio_to_text():
            #need to go on website to s3 to create bucket
            s3 = boto3.client('s3')
            try:
                bucket_name = 'languagelearn'
                file_path = '/Users/snowyan/PycharmProjects/learn/learn/input.mp3'  # Replace with the actual file path
                object_name = 'input.mp3'  # Replace with the desired object key

                s3.upload_file(file_path, bucket_name, object_name)
                print("File uploaded successfully")
            except NoCredentialsError:
                print("Credentials not available")


            # Create a Amazon Transcribe client
            transcribe = boto3.client('transcribe')

            # Specify the S3 URI of the audio file you want to transcribe
            audio_uri = 's3://languagelearner/input.mp3'

            # # Start the transcription job
            # transcribe.start_transcription_job(
            #     TranscriptionJobName='YourTranscriptionJobName',
            #     Media={'MediaFileUri': audio_uri},
            #     MediaFormat='mp3',  # Update this according to your audio file format
            #     LanguageCode='fr-FR'  # Update this according to the spoken language
            # )

            # # Wait for the transcription job to complete
            # while True:
            #     response = transcribe.get_transcription_job(
            #         TranscriptionJobName='YourTranscriptionJobName'
            #     )
            #     if response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            #         break

            # # Get the transcription results
            # if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            #     transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            #     transcript = transcribe.get_object(Bucket='your-bucket', Key=transcript_uri.split('/')[-1])['Body'].read().decode('utf-8')
            #     print(transcript)
            # else:
            #     print("Transcription job failed.")




#------------------------------------------------------------------------------------------------------------------------------------

class Chat:
    def __init__(self, conversation_list=[]) -> None:
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        # self.conversation_list = [{'role':'system','content':'你是一个非常友善的助手'}]
        self.conversation_list = []  # 初始化对话列表
        self.costs_list = []  # 初始化聊天开销列表
    
    def response_speaker(self, text):
        # Create a Polly client
        polly = boto3.client("polly")

        try:
            # Request speech synthesis
            response = polly.synthesize_speech(
                Text=text,
                OutputFormat="mp3",
                VoiceId="Mathieu"
            )
            
            # Access the audio stream from the response
            audio_stream = response["AudioStream"].read()

            # Save the audio stream to a file
            with open("output.mp3", "wb") as file:
                file.write(audio_stream)

            print("Speech synthesis successful. Audio saved as 'output.mp3'")
        except Exception as e:
            print("Error:", e)

                    
            # 打印对话
    def show_conversation(self, msg_list):
        for msg in msg_list[-2:]:
            if msg['role'] == 'user':  # 如果是用户的话
                # print(f"\U0001f47b: {msg['content']}\n")
                pass
            else:  # 如果是机器人的话
                message = msg['content']
                print(f"\U0001f47D: {message}\n")
                self.response_speaker(message)
            print()
    
   

    # 调用chatgpt，并计算开销
    def ask(self, prompt):
        self.conversation_list.append({"role": "user", "content": prompt})
        openai.api_key = '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'
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list)
        answer = response.choices[0].message['content']
        # 下面这一步是把chatGPT的回答也添加到对话列表中，这样下一次问问题的时候就能形成上下文了
        self.conversation_list.append({"role": "assistant", "content": answer})
        self.show_conversation(self.conversation_list)

        人民币花费 = total_counts(response)
        self.costs_list.append(人民币花费)
        print()
    
#------------------------------------------------------------------------------------------------------------------------------------

def total_counts(response):

        # 计算本次任务花了多少钱和多少tokens：
        tokens_nums = int(response['usage']['total_tokens'])  # 计算一下token的消耗
        price = 0.002 / 1000  # 根据openai的美元报价算出的token美元单价
        人民币花费 = '{:.5f}'.format(price * tokens_nums * 7.5)
        合计内容 = f'本次对话共消耗了{tokens_nums}个token，花了{人民币花费}元（人民币）'
        print(合计内容)

        return float(人民币花费)

#------------------------------------------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    output_wav = "recorded_audio.wav"
    input = "input.mp3"
    a = Audio()
    talk = Chat()
    
    # Define the WAV and MP3 file names
    output_wav = "recorded_audio.wav"
    output_mp3 = "input.mp3"

    # Call the function to record audio

    a.record_audio_with_threshold(output_wav)
    
    # Load the recorded audio from the WAV file
    audio = AudioSegment.from_wav(output_wav)

    # Export the recorded audio as MP3 with the desired file name
    audio.export(output_mp3, format="mp3")

    # Print a message indicating the conversion is complete
    print("Conversion to MP3 complete.")
    print()
    count = 0
    count_limit = eval(input("你想要对话的次数是多少呢？\n(请输入数字即可)"))
    while count < count_limit:  # 上下文token数量是有极限的，理论上只能支持有限轮次的对话，况且，钱花光了也就不能用了。。。
        if count < 1:
            words = input("请问有什么可以帮助你的呢？\n(请输入您的需求或问题)：")
        else:
            words = input("您还可以继续与我交流，请您继续说：\n(请输入您的需求或问题)：")
        print()
        talk.ask(words)
        #pygame.mixer.music.load("/Users/snowyan/PycharmProjects/learn/learn/output.mp3")
        try:
            # pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.load("/Users/snowyan/PycharmProjects/learn/learn/output.mp3")
            print("load")
            pygame.mixer.music.play()
            print("played")
        except pygame.error as e:
            print("An error occurred:", e)
        while pygame.mixer.music.get_busy():
            pass
        count += 1

    # g.msgbox("对不起，您已达到使用次数的限额，欢迎您下次使用！")
    print(f'本轮聊天合计花费{sum(talk.costs_list)}元人民币。')


if __name__ == "__main__":
    main()