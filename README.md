Video Subtitle Extraction Project

Overview
This web application is built using Django for backend processing and PostgreSQL for storing data, specifically focused on handling video subtitle extraction. The application allows users to upload videos, extract subtitles from them using ffmpeg, and store these subtitles in a PostgreSQL database. The app is containerized using Docker for easy deployment and development setup.

Features
1. Subtitle Extraction:
The application uses ffmpeg for extracting subtitles from uploaded videos.
Only ffmpeg is allowed for subtitle extraction—no other external services or libraries are used.
Subtitles are extracted in .srt format and then converted to .vtt format for web compatibility.
The ffprobe utility is used to detect subtitle streams from the video files.
Download ffmpeg from this link.
2. Docker Setup:
The entire application, including the Django backend and PostgreSQL database, is containerized using Docker.
A docker-compose.yml file is provided to facilitate easy setup for development.
The Docker container encapsulates Django, PostgreSQL, and the environment required for running the application.
To set up the environment, you can use the following command:

docker-compose up --build

3. Backend (Django):
The backend is developed using Django, and the main task is to handle video uploads, extract subtitles, and store both the video and subtitles in the database.
The subtitles are saved in the media folder, and their metadata is stored in a PostgreSQL database.

4. Frontend:
The UI for this application is minimalistic and simple since the evaluation focuses on the backend logic with Django and PostgreSQL.
The front-end allows users to upload videos, view the list of processed videos, and search through extracted subtitles.

5. Storage:
Uploaded videos are stored in the media directory as specified in the Django settings.
Extracted subtitles (in .vtt format) are also stored in the media folder, and their paths, along with other metadata (language, stream index), are saved in the PostgreSQL database.

6. Test Case:
A sample video is provided for testing, and the application is required to process and handle this video.
The goal is for the app to extract subtitles from the video, save them in the media folder, and store relevant information in the database.

Code Explanation

Video Upload and Subtitle Extraction
The main function to handle video uploads is upload_video(request).
When a video is uploaded, the form is validated, and the video is saved. The video path is then passed to the extract_subtitles_from_video() function.

Subtitle Extraction Logic
Subtitle Probing:

The function probe_subtitles(video_path) uses ffprobe to find available subtitle streams in the uploaded video.
It extracts the stream index and language of each subtitle stream.
Extracting Subtitles:

The function extract_subtitle(video_path, stream_index) is responsible for running the ffmpeg command to extract subtitles for each subtitle stream into .srt files.
The convert_srt_to_vtt() function converts the extracted .srt files to .vtt format, which is more suitable for web use.
Database Storage:

The extracted subtitles are saved in the media folder. For each subtitle, a Subtitle object is created in the database, which includes the video, the subtitle file path, the language, and the stream index.
Search Functionality
The application allows searching through subtitles using the search_subtitles(subtitle_path, query, language) function.
Users can search for specific text within subtitle files, and the application returns the results, including the timestamp and subtitle text.

Error Handling
The application includes basic error handling for:
Issues during subtitle extraction.
File I/O operations (reading and writing subtitle files).
Searching within subtitle files.
Commands for Running the Application:

Run the application using Docker:
Ensure you have Docker installed.
Clone the repository:
git clone https://github.com/hdhankecha/Video_fatmug.git

Build and start the Docker containers:
docker-compose up --build

Access the application at http://localhost:8000.
Without Docker: If you want to run the application without Docker:

pip install -r requirements.txt

Set up PostgreSQL and configure the Django settings.py.

Run migrations:
python manage.py migrate

Start the Django development server:
python manage.py runserver
