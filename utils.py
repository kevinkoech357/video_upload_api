import os
import moviepy.editor as mp
import assemblyai
import pysrt
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access the AssemblyAI API key using os.environ
ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")

# Initialize the AssemblyAI client
assemblyai.api_key = ASSEMBLYAI_API_KEY

# ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov', 'webm'}

# Helper function to check if the file extension is allowed
# def allowed_file(filename):
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_video(video_path):
    try:
        # Load the video using MoviePy
        video_clip = mp.VideoFileClip(video_path)

        # Extract audio from the video
        audio_clip = video_clip.audio

        # Save the audio to a temporary file
        with open("temp_audio.wav", "wb") as f:
            audio_clip.write_audiofile(f, codec="pcm_s16le")

        # Transcribe the audio using AssemblyAI
        response = assemblyai.Transcribe.create(audio_url="temp_audio.wav")

        # Wait for the transcription to complete (this may take a while)
        response.wait()

        # Get the transcription text
        transcription_text = response.get()["text"]

        # Delete the temporary audio file
        os.remove("temp_audio.wav")

        return transcription_text
    except Exception as e:
        return str(e)


def generate_srt_subtitle(subtitle_filepath, transcription_text):
    try:
        # Create a SubRipFile
        subs = pysrt.SubRipFile()

        # Split the transcription text into chunks of text for subtitles (adjust the chunk duration as needed)
        chunk_duration = 5  # in seconds
        start_time = pysrt.SubRipTime(0, 0, 0)
        end_time = pysrt.SubRipTime(0, 0, chunk_duration)

        text_chunks = [transcription_text[i:i + chunk_duration] for i in range(0, len(transcription_text), chunk_duration)]

        # Add subtitles based on text chunks
        for i, chunk in enumerate(text_chunks):
            subs.append(pysrt.SubRipItem(index=i + 1, start=start_time, end=end_time, text=chunk, text_styles={"font": "Arial", "size": 16, "color": "#000000"}))
            start_time = end_time
            end_time = end_time + pysrt.SubRipTime(0, 0, chunk_duration)

        # Save the SRT subtitle file
        subs.save(subtitle_filepath, encoding="utf-8")

    except Exception as e:
        return str(e)
