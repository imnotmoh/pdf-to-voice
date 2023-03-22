import os
import time

import requests






def audio(text):

    url = "https://large-text-to-speech.p.rapidapi.com/tts"
    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": os.environ.get('large_text_api_key'),
	"X-RapidAPI-Host": "large-text-to-speech.p.rapidapi.com"
    }

    body = {
        "text":f"{text}"
    }
    # make request to the api
    response = requests.post(url=url,headers=headers,json=body)
    response.raise_for_status()
    # to wait for the api to process the text to audio
    time.sleep(response.json().get("eta") + 15)

    param  = {
        "id":response.json().get("id")
    }
    # get the url of the audio
    audio_url = requests.get(url,params=param, headers=headers)
    audio_url.raise_for_status()
    # returns the url
    return [audio_url.json().get("url"),audio_url.json().get("id")]



def play_audio(url):
    import pygame
    # download the Wav file from the response_URL
    response = requests.get(url[0])
    open(f"{url[1]}.wav", 'wb').write(response.content)
    from pydub import AudioSegment
    from pydub.playback import play
    # play the audio
    audio = AudioSegment.from_wav(f"{url[1]}.wav")
    play(audio)


def pdf_to_string(doc:str):
    # process the pdf
    import PyPDF2
    with open(doc,'rb') as file:
        pdfreader = PyPDF2.PdfReader(file)
        # convert it into an api readable format
        string = pdfreader.pages[0].extract_text()
        strip = [i.strip() for i in string.split()]
        return ' '.join(strip)



text = pdf_to_string("Document 4-2.pdf")
audio = audio(text)
play_audio(audio)






