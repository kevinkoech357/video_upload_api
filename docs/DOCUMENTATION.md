# API Documentation

This API allows users to upload videos, transcribe their audio content, and generate SRT subtitles for the videos. It provides endpoints for uploading videos, accessing the list of uploaded videos, serving video files, and serving SRT subtitle files.

## Base URL

The base URL for all API endpoints is `/api`.

## Table of Contents

1. [Upload a Video](#1-upload-a-video)
2. [List All Uploaded Videos](#2-list-all-uploaded-videos)
3. [Serve a Video](#3-serve-a-video)
4. [List All Uploaded Videos (Alternate View)](#4-list-all-uploaded-videos-alternate-view)
5. [Serve SRT Subtitles](#5-serve-srt-subtitles)

## 1. Upload a Video

**Endpoint:** `/upload`

**HTTP Method:** POST

**Description:** Upload a video file for transcription and subtitle generation.

**Request Body:**

- `file` (multipart/form-data): The video file to be uploaded.

**Response:**

- Status Code: 200 (OK) or 400 (Bad Request) or 500 (Internal Server Error)
- Content Type: JSON

**Response Body (Success):**

```json
{
  "message": "File uploaded successfully",
  "video_url": "/api/serve_video/<video_name>",
  "subtitles_url": "/api/serve_subtitles/<subtitle_name>"
}
```
Response Body (Error - Missing Filename):

```bash
{
  "message": "Missing filename. Please provide a valid filename for the video."
}
```
Response Body (Error - Unsupported Format):

```bash
{
  "message": "File is not a video"
}
```
Response Body (Error - Unsupported Video Format):

```bash
{
  "message": "Unsupported video format. Please upload a video in one of the supported formats: mp4, avi, mkv, etc."
}
```
Response Body (Error - Internal Server Error):

```
{
  "message": "An error occurred: <error_message>"
}
```
2. List All Uploaded Videos
Endpoint: /all_videos

HTTP Method: GET

Description: Retrieve a list of all uploaded videos.

Response:

Status Code: 200 (OK) or 500 (Internal Server Error)
Content Type: HTML
Response Body (Success):

HTML page displaying a list of uploaded video files.

Response Body (Error - Internal Server Error):

HTML page displaying an error message.

3. Serve a Video
Endpoint: /serve_video/<string:video_name>

HTTP Method: GET

Description: Serve an uploaded video by its name.

URL Parameters:

video_name (string): The name of the video file to serve.
Response:

Status Code: 200 (OK) or 404 (Not Found) or 500 (Internal Server Error)
Response Body (Error - Video Folder Not Found):

```bash
{
  "message": "Video folder not found"
}
```
Response Body (Error - Video Not Found):

```
{
  "message": "Video not found"
}
```
Note: The video file will be streamed as the response.

4. List All Uploaded Videos (Alternate View)
Endpoint: /all_videos_list

HTTP Method: GET

Description: Retrieve a list of all uploaded videos in an alternate view.

Response:

Status Code: 200 (OK) or 500 (Internal Server Error)
Content Type: HTML
Response Body (Success):

HTML page displaying a list of uploaded video files in an alternate view.

Response Body (Error - Internal Server Error):

HTML page displaying an error message.

5. Serve SRT Subtitles
Endpoint: /serve_subtitles/<string:subtitle_name>

HTTP Method: GET

Description: Serve an SRT subtitle file by its name.

URL Parameters:

subtitle_name (string): The name of the SRT subtitle file to serve.
Response:

Status Code: 200 (OK) or 404 (Not Found) or 500 (Internal Server Error)
Response Body (Error - Subtitles Folder Not Found):

```bash
{
  "message": "Subtitles folder not found"
}
```
Response Body (Error - Subtitles Not Found):

```bash
{
  "message": "Subtitles not found"
}
```
Note: The SRT subtitle file will be served as the response.

Error Handling
In case of errors, the API will return a JSON response with an error message and an appropriate HTTP status code.
Internal server errors (HTTP 500) may occur due to unexpected issues and will include an error message for debugging.
Usage Notes
Videos should be uploaded in common video formats such as MP4, AVI, MKV, etc.
The uploaded videos will be transcribed, and subtitles will be generated automatically.
Generated subtitles will be served in SRT format.

### Example Usage
Use the /upload endpoint to upload a video file.
Access the list of uploaded videos using /all_videos or /all_videos_list.
Serve a specific video using /serve_video/<video_name>.
Serve subtitles for a video using /serve_subtitles/<subtitle_name>.
Note: Replace <video_name> and <subtitle_name> with the actual names of the video and subtitle files.
