from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
# import mimetypes
from utils import generate_srt_subtitle, extract_audio_from_video
from flask_cors import CORS
import assemblyai as aai

app = Flask(__name__, template_folder="templates")
CORS(app)

aai.settings.api_key = f"fd3f4248151d4181a2299f79bf2c7b42"

# Define the path to the static folder for storing user-uploaded videos
UPLOAD_FOLDER = 'static/videos'
SUBTITLES_FOLDER = 'static/subtitles'
AUDIO_TEMP_FOLDER = 'static/audio_temp'  # Temporary folder for audio extraction
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SUBTITLES_FOLDER'] = SUBTITLES_FOLDER
app.config['AUDIO_TEMP_FOLDER'] = AUDIO_TEMP_FOLDER


@app.route('/api/upload', methods=['POST'])
def upload_video():
    try:
        #if 'file' not in request.files:
        # return jsonify(
        #        {
        #            "status": "error",
        #            "message": "No video file uploaded!"
        #        }
        #    )

        file = request.files['file']
        # Check if the filename is missing
        if not file.filename:
            return jsonify(
                {
                    "message": "Missing filename. Please provide a valid filename for the video."
                }
            ), 400

        filename = secure_filename(file.filename)

        # Check if file type is in video format
        # mimetype = mimetypes.guess_type(filename)[0]
        # if not mimetype or not mimetype.startswith('video'):
        #   return jsonify({"message": "File is not a video"})

        # Check if the file has an allowed extension
        # if not allowed_file(filename):
        #    return jsonify(
        #        {
        #            "message": "Unsupported video format. Please upload a video in one of the supported formats: " + ", ".join(ALLOWED_EXTENSIONS)
        #        }
        #    ), 400


        # Define directory path to save videos and subtitles
        video_uploads_folder = os.path.join(app.config['UPLOAD_FOLDER'])
        subtitles_folder = os.path.join(app.config['SUBTITLES_FOLDER'])
        audio_temp_folder = os.path.join(app.config['AUDIO_TEMP_FOLDER'])

        # Check if the directories exist, if not, create them
        if not os.path.exists(video_uploads_folder):
            os.makedirs(video_uploads_folder)
        if not os.path.exists(subtitles_folder):
            os.makedirs(subtitles_folder)
        if not os.path.exists(audio_temp_folder):
            os.makedirs(audio_temp_folder)

        # Define the full file paths
        video_filepath = os.path.join(video_uploads_folder, filename)
        subtitles_filepath = os.path.join(subtitles_folder, os.path.splitext(filename)[0] + '.srt')
        audio_temp_filepath = os.path.join(audio_temp_folder, os.path.splitext(filename)[0] + '.wav')

        # Save the video file to the directory
        file.save(video_filepath)

       # Extract the audio from the video file
        audio_temp_filepath = extract_audio_from_video(video_filepath)

        # Transcribe the audio file
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_temp_filepath)

        # Generate and save the .srt subtitle file
        generate_srt_subtitle(subtitles_filepath, transcript)

        # Generate URLs for video and subtitles
        video_url = url_for('serve_video', video_name=filename)
        subtitles_url = url_for('serve_subtitles', subtitle_name=os.path.basename(subtitles_filepath))

        return jsonify(
            {
                "message": "File uploaded successfully",
                "video_url": video_url,
                "subtitles_url": subtitles_url
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred: " + str(e)
            }
        ), 500


@app.route('/api/all_videos', methods=['GET'])
def all_videos():
    try:
        video_uploads_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(video_uploads_folder):
            return render_template('videos.html', videos=[])

        video_files = [f for f in os.listdir(video_uploads_folder) if any(f.endswith(ext) for ext in ['.mp4', '.avi', '.mkv', '.wmv'])]
        return render_template('videos.html', videos=video_files)
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@app.route('/api/serve_video/<string:video_name>', methods=['GET'])
def serve_video(video_name):
    try:
        video_uploads_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(video_uploads_folder):
            return jsonify({"message": "Video folder not found"}), 404

        video_path = os.path.join(video_uploads_folder, video_name)
        if not os.path.exists(video_path):
            return jsonify({"message": "Video not found"}), 404

        return send_from_directory(video_uploads_folder, video_name)
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@app.route('/api/all_videos_list', methods=['GET'])
def all_videos_list():
    try:
        video_uploads_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(video_uploads_folder):
            return jsonify({"message": "Video folder not found"}), 404

        video_files = [f for f in os.listdir(video_uploads_folder) if any(f.endswith(ext) for ext in ['.mp4', '.avi', '.mkv', '.wmv'])]
        return render_template('videos_list.html', video_files=video_files)
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500


@app.route('/api/serve_subtitles/<string:subtitle_name>', methods=['GET'])
def serve_subtitles(subtitle_name):
    try:
        subtitles_folder = app.config['SUBTITLES_FOLDER']
        if not os.path.exists(subtitles_folder):
            return jsonify({"message": "Subtitles folder not found"}), 404

        subtitle_path = os.path.join(subtitles_folder, subtitle_name)
        if not os.path.exists(subtitle_path):
            return jsonify({"message": "Subtitles not found"}), 404

        # Serve the subtitle file
        return send_from_directory(subtitles_folder, subtitle_name)
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
