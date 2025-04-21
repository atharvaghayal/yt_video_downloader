from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp
import os

app = FastAPI()

# Serve static files (CSS, JS) correctly from "ui" folder
app.mount("/static", StaticFiles(directory="ui"), name="static")

class VideoRequest(BaseModel):
    url: str

@app.get("/")
async def get_home():
    # Serve the index.html file
    return FileResponse("ui/index.html")

@app.post("/download/")
async def download_video(request: VideoRequest):
    try:
        # Set download options
        options = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s'  # Save in the downloads folder (this is temp)
        }
        
        # Start downloading with yt-dlp
        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(request.url, download=True)
        
        # Return the URL of the video
        video_path = f"downloads/{result['title']}.{result['ext']}"
        return {"download_url": video_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")