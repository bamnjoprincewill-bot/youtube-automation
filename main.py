from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import json
from googleapiclient.http import MediaFileUpload
youtube = build("youtube", "v3", credentials=creds)
creds = Credentials.from_authorized_user_info(
    creds_dict, 
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)
# Load credentials from environment variable
creds_json = os.environ.get("YOUTUBE_OAUTH_JSON")
if creds_json:
    creds_data = json.loads(creds_json)
    creds = Credentials.from_authorized_user_info(creds_data)
else:
    raise Exception("YouTube OAuth credentials not found")
# Load OAuth JSON from GitHub Secrets
oauth_json = os.environ.get("YOUTUBE_OAUTH_JSON")
creds_dict = json.loads(oauth_json)
import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from googleapiclient.discovery import build
from datetime import datetime
import random

# -----------------------------
# CONFIG
# -----------------------------
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
CHANNEL_ID = 'YOUR_CHANNEL_ID'
VIDEO_OUTPUT = "output.mp4"  # Path to your generated video

video_file = "path_to_your_video.mp4"  # <-- replace with actual file name or variable

VIDEO_DURATION = 15  # seconds per image
IMAGE_FOLDER = 'images/'  # folder with free stock images
SCRIPT_TOPICS = ['Tech gadgets', 'Smart home accessories', 'AI tools', 'Mobile apps']

# -----------------------------
# STEP 1: Generate Script (Using OpenAI free API alternative)
# -----------------------------
def generate_script(topic):
    # Use OpenAI GPT API if you have access, or manually set script
    # Example simple script:
    return f"Today we will talk about {topic}. Stay tuned for amazing insights!"

# -----------------------------
# STEP 2: Generate Voice
# -----------------------------
def text_to_speech(script_text):
    tts = gTTS(text=script_text, lang='en')
    audio_file = 'voice.mp3'
    tts.save(audio_file)
    return audio_file

# -----------------------------
# STEP 3: Collect Images
# -----------------------------
def get_images(n=5):
    # Use local folder images, or download free stock images automatically
    images = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.jpg','.png'))]
    return random.sample(images, min(n, len(images)))

# -----------------------------
# STEP 4: Create Video
# -----------------------------
def create_video(audio_file, images):
    audio = AudioFileClip(audio_file)
    clips = []
    for img in images:
        clip = ImageClip(img).set_duration(VIDEO_DURATION)
        clips.append(clip)
    video = concatenate_videoclips(clips)
    video = video.set_audio(audio)
    video.write_videofile(VIDEO_OUTPUT, fps=24)
    return VIDEO_OUTPUT

# -----------------------------
# STEP 5: Upload to YouTube
# -----------------------------
def upload_youtube(video_file, title, description, tags=[]):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "28"  # Science & Technology
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=video_file
    )
    response = request.execute()
    print(f"Uploaded Video: {response['id']}")
    return response['id']

# -----------------------------
# STEP 6: Run Workflow
# -----------------------------
def run_workflow():
    topic = random.choice(SCRIPT_TOPICS)
    script = generate_script(topic)
    audio_file = text_to_speech(script)
    images = get_images()
    video_file = create_video(audio_file, images)
    title = f"{topic} - Amazing Facts!"
    description = f"This video is about {topic}. Enjoy!"
    upload_youtube(video_file, title, description, tags=['tech','gadgets','AI'])
    print("Workflow Completed at", datetime.now())

# Run the workflow
if __name__ == "__main__":
    run_workflow()
