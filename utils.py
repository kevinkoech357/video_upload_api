import os
import pysrt



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


