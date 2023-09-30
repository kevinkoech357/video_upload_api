
## API Documentation

### Overview

This API provides endpoints for uploading, viewing, and serving user-uploaded videos.

### Endpoints

* **Upload video:** `/upload/<username>`
* **View all videos for a user:** `/all_videos/<username>`
* **Serve a video:** `/serve_video/<username>/<video_name>`

### Request methods

* **Upload video:** `POST`
* **View all videos for a user:** `GET`
* **Serve a video:** `GET`

### Request parameters

* **Upload video:** `file` (required)

### Responses

* **Upload video:**
    * `200 OK`: Video uploaded successfully.
    * `400 Bad Request`: No file uploaded.
* **View all videos for a user:**
    * `200 OK`: List of all uploaded videos for the user.
    * `404 Not Found`: User folder not found.
* **Serve a video:**
    * `200 OK`: Video streamed to the user's browser.
    * `404 Not Found`: Video not found.

### Example requests and responses

**Test upload using curl**

Test upload using curl
curl -X POST http://localhost:5000/upload/johndoe -F file=@my_video.mp4


HTTP/1.1 200 OK
Content-Type: application/json

{
"message": "File uploaded successfully"
}


**Test view all videos for a user**

Test view all videos for a user
curl http://localhost:5000/all_videos/johndoe


HTTP/1.1 200 OK
Content-Type: application/json

[
{
"filename": "my_video.mp4",
"upload_date": "2023-09-30T12:00:00Z"
}
]


**Test serve a video**

Test serve a video
curl http://localhost:5000/serve_video/johndoe/my_video.mp4


HTTP/1.1 200 OK
Content-Type: video/mp4


### Error responses

**Upload video**

HTTP/1.1 400 Bad Request
Content-Type: application/json

{
"message": "No file uploaded"
}


**View all videos for a user**

HTTP/1.1 404 Not Found
Content-Type: application/json

{
"message": "User folder not found"
}


**Serve a video**

HTTP/1.1 404 Not Found
Content-Type: application/json

{
"message": "Video not found"
}


### Testing the API with curl

To test the API with curl, you can use the following commands:

Test upload using curl
curl -X POST http://localhost:5000/upload/johndoe -F file=@my_video.mp4


Test view all videos for a user
curl http://localhost:5000/all_videos/johndoe


Test serve a video
curl http://localhost:5000/serve_video/johndoe/my_video.mp4


**Note:** Replace `my_video.mp4` with the name of the video file that you want to upload or serve.

### Troubleshooting

If you are having trouble using the API, please check the following:

* Make sure that you are using the correct request method and endpoint.
* Make sure that you are providing all of the required request parameters.
* Make sure that you are uploading videos in MP4 format.
* Make sure that the videos that you are uploading are saved to the user's upload folder.

If you are still having trouble, please open an issue on the GitHub repository.
