from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import re
from fastapi import FastAPI
import sentry_sdk
from dotenv import load_dotenv
import os

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv('DNS-SENTRY'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


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

@app.get("/search/")
async def root(param):
    def extract_video_ids(html_content):
        soup = BeautifulSoup(html_content, 'lxml')

        video_ids = []

        for match in re.findall(r'"videoId":"(\w+)"', html_content):
            video_ids.append(match)

        return video_ids

    def get_ids(response):
        if isinstance(response.content, bytes):
            response_content = response.content.decode('utf-8')
        else:
            response_content = response.content

        video_ids = extract_video_ids(response_content)
        seen_items = set()  
        unique_list = []

        for item in video_ids:
            if item not in seen_items: 
                seen_items.add(item)  
                unique_list.append(item) 

        return(unique_list[:1])


    url = "https://youtube.com/results?search_query="+param 
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        result = get_ids(response) 
        return result
    else:
        return(f"Failed to access URL: {response.status_code}")


