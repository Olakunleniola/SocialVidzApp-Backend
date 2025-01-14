<img src="https://res.cloudinary.com/dhlmazrcf/image/upload/v1736441584/pl9ef1srtx7i35pv3av2.png" alt="logo" width="350" > 

#
SocialVidz is a web service that allows users to download videos from various social media platforms without requiring login credentials. Simply paste the video URL, and the service will process the request, retrieve video information, and stream the video directly to the frontend. The application is designed to be lightweight and efficient by streaming videos directly to the client, minimizing server memory usage.

## Features

- Supports video downloads from popular social media platforms including YouTube, Facebook, Instagram, Twitter, LinkedIn, Reddit, and others.
- Fetches video details such as title, duration, uploader, size, and platform.
- Streams videos to the frontend to minimize memory usage on the server.
- Provides a simple API for integration into other applications or services.
- Environment-specific configurations for development (SQLite) and production (PostgreSQL) databases.
- Configured logging for development environments.

## Installation

### Prerequisites

1. Python 3.8 or later
2. Virtual environment (optional but recommended)

### Steps

1. Clone the repository:


   ```bash
      git clone https://github.com/Olakunleniola/SocialVidzApp-Backend.git
      cd social-vidz
   ``` 

2. Create and activate a virtual environment:

- For Linux/macOS:

   ```bash
      python3 -m venv .myvenv
      source .myvenv/bin/activate
   ```
- For Windows:
   ```bash
      python -m venv .myvenv
      .myvenv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
      pip install -r requirements.txt
      Set up environment variables:
   ```

4. Ensure that the DATABASE_URL is set according to your environment (SQLite for development, PostgreSQL for production).

## Running the Application
To run the FastAPI application, use the following command:

   ```bash
   uvicorn app.main:app --reload
   ```

> By default, the application will be accessible at http://127.0.0.1:8000.

## API Endpoints

#### 1. Get Video Information

- **URL**: /api/info
- **Method**: GET
- **Query Parameters**: url: The URL of the video (e.g., YouTube, Instagram)
- **Response**:

   ```json
   {
   "status": "success",
   "data": {
      "title": "Video Title",
      "url": "Video URL",
      "platform": "YouTube",
      "duration": 120,
      "uploader": "Uploader Name",
      "size": 450000000
   }
   }
   ```
#### 2. Download Video
- **URL:** /api/download
- **Method:** POST
- **Request Body:**
   ```json
   {
   "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
   "platform": "youtube",
   "title": "Sample Video"
   }
   ```
- **Response:** The video will be streamed directly to the client as an attachment (.mp4 file).

## Future Work
- Support additional video platforms.
- Implement authentication and user management (if needed in future).
- Improve error handling and custom error messages.
- Add user rate limiting to prevent abuse of the service.

## License
This project is licensed under the MIT License - see the [LICENSE](https://) file for details.

## Acknowledgments
Thanks to the yt-dlp project for providing a powerful and flexible tool for downloading videos.
FastAPI for being a fast, efficient, and easy-to-use framework for building APIs.