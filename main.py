from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import mimetypes

app = Flask(__name__, template_folder="templates")

# Define the path to the static folder for storing user-uploaded videos
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload/<string:user_name>', methods=['POST'])
def upload_video(user_name):
    try:
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)

            # Check if file type is in video format
            mimetype = mimetypes.guess_type(filename)[0]
            if not mimetype or not mimetype.startswith('video'):
                return jsonify({"message": "File is not a video"})

            # Define directory path to save user's videos
            user_uploads_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_name)

            # Check if the directory exists, if not, create it
            if not os.path.exists(user_uploads_folder):
                os.makedirs(user_uploads_folder)

            # Define the full file path
            filepath = os.path.join(user_uploads_folder, filename)

            # Save the file to the directory
            file.save(filepath)

            return jsonify({"message": "File uploaded successfully"}), 200
        return jsonify({"message": "No file uploaded"}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500


@app.route('/all_videos/<string:user_name>', methods=['GET'])
def all_videos(user_name):
    try:
        user_uploads_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_name)
        if not os.path.exists(user_uploads_folder):
            return render_template('videos.html', videos=[], user_name=user_name)

        video_files = [f for f in os.listdir(user_uploads_folder) if f.endswith('.mp4')]
        return render_template('all_videos.html', videos=video_files, user_name=user_name)
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@app.route('/serve_video/<string:user_name>/<string:video_name>', methods=['GET'])
def serve_video(user_name, video_name):
    try:
        user_uploads_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_name)
        if not os.path.exists(user_uploads_folder):
            return jsonify({"message": "User folder not found"}), 404

        video_path = os.path.join(user_uploads_folder, video_name)
        if not os.path.exists(video_path):
            return jsonify({"message": "Video not found"}), 404

        return send_from_directory(user_uploads_folder, video_name)
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
