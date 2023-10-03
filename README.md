# Overview

This is a simple Flask app for uploading, viewing, and serving user-uploaded videos.

## Features

* Upload videos in MP4 format
* View a list of all uploaded videos for a given user
* Serve videos to users

## Usage

### To upload a video:

* Visit /api/upload/.
* Select the video file that you want to upload and click the "Upload" button.

The video will be saved to the user's upload folder.

### To view a list of all uploaded videos for a given user:

* Visit /api/all_videos/

You will see a list of all uploaded videos for the user, with the filename and upload date.

### To serve a video:

* Visit /serve_video/<video_name>, where <video_name> is the filename of the video.
* The video will be streamed to the user's browser.

### Requirements

Python 3.6+
Flask

### Installation
```bash
#Clone the repository:
git clone https://github.com/kevinkoech357/video-upload-api.git
#Change directory into the project directory:
cd video-upload-api
#Install the dependencies:
pip install -r requirements.txt
```

### Running the app
```bash
#Start the app:
python app.py
```
The app will be running on http://localhost:5000.

### Example usage

To upload a video for the user "johndoe":
```bash
curl -X POST http://localhost:5000/api/upload/johndoe -F file=@my_video.mp4
```
To view a list of all uploaded videos for the user "johndoe":
```bash
curl http://localhost:5000/api/all_videos/johndoe
```
To serve the video "my_video.mp4" that was uploaded by the user "johndoe":
```bash
curl http://localhost:5000/api/serve_video/my_video.mp4
```

### Troubleshooting

If you are having trouble with the app, please check the following:

* Make sure that you have installed all of the required dependencies.
* Make sure that the app is running on the correct port.
* Make sure that you are uploading videos in MP4 format.
* Make sure that the videos that you are uploading are saved to the user's upload folder.
* If you are still having trouble, please open an issue on the GitHub repository.
