import os

import requests
import vlc
from playsound import playsound






def audio(text):
    url = "https://cloudlabs-text-to-speech.p.rapidapi.com/synthesize"
    header = {
        'X-RapidAPI-Key': os.environ.get('cloudlad_apikey'),
        'X-RapidAPI-Host': 'cloudlabs-text-to-speech.p.rapidapi.com',
    }
    body = {
        "voice_code": "en-US-1",
        "text": f"{text}"
    }
    response = requests.post(url=url, data=body, headers=header)
    response.raise_for_status()
    return response.json()['result']['audio_url']


def play_audio(url):
    print(url.split()[-1])
    import pygame
    # download the MP3 file from the URL
    response = requests.get(url)
    open(url.split('/')[-1], 'wb').write(response.content)

    # initialize pygame mixer
    pygame.mixer.init()

    # load the MP3 file
    pygame.mixer.music.load(url.split('/')[-1])

    # play the MP3 file
    pygame.mixer.music.play()

    # keep the program running until the music ends
    while pygame.mixer.music.get_busy():
        continue


def pdf_to_string(doc:str):
    import PyPDF2
    with open(doc,'rb') as file:
        pdfreader = PyPDF2.PdfReader(file)

        return pdfreader.pages[0].extract_text()

text = pdf_to_string("Document 4-2.pdf")

audio = audio(text)
play_audio(audio)
