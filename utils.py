import os
import openai
import ffmpeg
import pysrt
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access the API key using os.environ
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov'}

openai.api_key = OPENAI_API_KEY

# Helper function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_video(video_path, audio_temp_path):
    try:
        # Use ffmpeg-python to extract audio from the video
        (
            ffmpeg.input(video_path)
            .output(audio_temp_path)
            .run()
        )

        # Read the extracted audio
        with open(audio_temp_path, 'rb') as audio_file:
            audio_content = audio_file.read()

        # Transcribe the audio using Whisper
        response = openai.Transcription.create(
            audio=audio_content,
            model="whisper",
            language="en-US"
        )

        # Get the transcription text
        transcription_text = response['text']

        # Delete the temporary audio file to avoid collisions
        os.remove(audio_temp_path)

        return transcription_text
    except Exception as e:
        return str(e)

def generate_srt_subtitle(subtitle_filepath, transcription_text):
    try:
        # Create an SRT file and add subtitles based on the transcription
        subs = pysrt.SubRipFile()
        subs.append(pysrt.SubRipItem(index=1, start=pysrt.SubRipTime(0, 0, 0), end=pysrt.SubRipTime(0, 0, 5), text=transcription_text))
        subs.save(subtitle_filepath, encoding='utf-8')

    except Exception as e:
        return str(e)

