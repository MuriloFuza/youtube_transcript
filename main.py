from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = FastAPI()


@app.get("/transcript/")
async def root(video_link, language):

    idYoutube = re.search(r"(?:(?:https?://)?(?:www\.)?youtube\.com/(?:(?:v/)?(?:watch\?v=)?|embed/))([\w-]+)", video_link).group(1)

    try:
        youtube = YouTubeTranscriptApi.get_transcript(idYoutube, languages=[language])
    except: 
        return {"Nao existem legendas neste idioma para este video"}

    newArrayString = ''
    for message in youtube: 
        newArrayString += ' ' + message['text']


    return {newArrayString}