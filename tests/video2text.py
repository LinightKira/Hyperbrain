# pip install moviepy speechrecognition pydub
# 提取视频中的内容 转为文案 目前只能视频分离音频
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment

"""
Extracts audio from a video file, converts it to text using Google Speech Recognition,
and saves the text to a file.

Parameters:
- video_file_path: str, the path to the video file.
- output_file_path: str, optional, the path to save the text file. If not provided, a default path is used.

Returns:
- output_file_path: str, the path where the text file is saved.
"""


def video_to_text(video_file_path, output_file_path=None):
    # Ensure the provided path exists
    if not os.path.exists(video_file_path):
        raise FileNotFoundError(f"The path {video_file_path} does not exist.")

    # Extract the audio from the video
    video = VideoFileClip(video_file_path)
    audio_path = video_file_path.rsplit('.', 1)[0] + '.wav'
    video.audio.write_audiofile(audio_path)

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Convert audio file to text
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        # 语音转文本 还需要修改 0716
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            text = "Audio not clear enough to recognize."
        except sr.RequestError:
            text = "Could not request results from Google Speech Recognition service."

    # Determine output path
    if output_file_path is None:
        output_file_path = video_file_path.rsplit('.', 1)[0] + '.txt'

    # Save the text to a file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    # Clean up the audio file
    # os.remove(audio_path)

    return output_file_path


# Example usage:
# Replace 'path_to_video.mp4' with your actual video file path
video_path = 'test_video.mp4'
output_path = video_to_text(video_path)
print(f"Text extracted and saved to: {output_path}")
