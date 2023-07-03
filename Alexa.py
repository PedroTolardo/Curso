import speech_recognition as sr #pip install SpeechRecognition
import json
import spotipy #pip install spotipy
import webbrowser
import pyautogui as pa #pip install pyautogui
import time
#from playsound import playsound
#from gtts import gTTS
import pyaudio
import os
import pyttsx3 #pip install pyttsx3
from googlesearch import search #pip install google
from bs4 import BeautifulSoup #pip install BeautifulSoup
import requests

class VoiceAssistant:
    
    def __init__(self):
        self.keyword_hera = ["Alexa", "alexa", "Alex", "alex", "Alexia", "alexia", "game", "Game"]
        self.keyword_music = ["toque", "tocar", "música"]
        self.keyword_question = ["qual", "o que", "quando", "como", "quem", "Qual"]
        self.keyword_pass = ["próxima música"]
        self.keyword_pause = ["pausar música", "pause"]
        self.keyword_play = ["tocar", "continue"]
        self.r = sr.Recognizer()
        self.language = "pt-BR"
        self.username = 'pedro'
        self.clientID = '9843855025ed4f77a4b838d5e963350e'
        self.clientSecret = '6b5987c56f2a4c668e8caa0179720198'
        self.redirectURI = 'http://google.com/' 

    def record_audio(self, phrase_time_limit=2):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.r.adjust_for_ambient_noise(source, duration=1)
            audio = self.r.listen(source, phrase_time_limit=phrase_time_limit)
        return audio

    def transcribe_audio(self, audio):
        try:
            text = self.r.recognize_google(audio, language=self.language)
            print(text)
            return text
        except sr.UnknownValueError:
            val_err = "Sorry, I could not understand what you said."
            print(val_err)
            return val_err
        
    def speak(self, text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 180)
        engine.setProperty('voice', 'brazil')
        engine.say(text)
        engine.runAndWait()

    def recognize_alias(self):
        audio = self.record_audio()
        text = self.transcribe_audio(audio)
        text1 = text.split()
        for word in text1:
            if word in self.keyword_hera:
                print("Olá, em que posso ajudar?")
                self.speak("Olá, em que posso ajudar?")
                return True

    def config_spotify(self):
        self.oauth_object = spotipy.SpotifyOAuth(self.clientID,self.clientSecret,self.redirectURI)
        self.token_dict = self.oauth_object.get_access_token()
        self.token = self.token_dict['access_token']
        self.spotifyObject = spotipy.Spotify(auth=self.token)
        self.user = self.spotifyObject.current_user()
        
    def play_music(self):
        self.config_spotify()
        print("Qual música você deseja tocar?")
        self.speak("Qual música você deseja tocar?")
        audio = self.record_audio()
        text = self.transcribe_audio(audio)
        # Get the Song Name.
        searchQuery = text
        self.speak("Uau, essa é boa!")
        print('Tocando', text)
        self.speak('Tocando '+ text)
        # Search for the Song.
        searchResults = self.spotifyObject.search(text, 1, 0, "track")
        # Get required data from JSON response.
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        if tracks_items:
            song = tracks_items[0]['external_urls']['spotify']
            # Open the Song in Web Browser
            webbrowser.open(song)
            time.sleep(20)
            pa.moveTo(560, 695)
            pa.click()
        else:
            print("Nenhuma música encontrada.")
            self.speak("Nenhuma música encontrada.")
    
    def answer(self, text):
        query = text + " site:wikipedia.org"
        print(query)
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            print(f"Processing link: {j}")
            if "wikipedia.org" not in j:
                print("Not a Wikipedia link. Skipping...")
                continue
            link = j
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all('p')
            non_empty_paragraphs = [p for p in paragraphs if p.text.strip()]
            if len(non_empty_paragraphs) > 0:
                result = non_empty_paragraphs[0].text
                print(result)
                self.speak(result)
                break
            else:
                print("No non-empty paragraphs found.")

            
    def run(self):
        while True:
            alias = self.recognize_alias()
            while alias:
                audio = self.record_audio()
                text = self.transcribe_audio(audio)
                text1 = text.split()
                if any(word in self.keyword_music for word in text1):
                    self.play_music()
                elif any(word in self.keyword_question for word in text1):
                    self.answer(text)
                alias = False  # Add this line to exit the inner loop and check for alias again in the outer loop

                
if __name__ == '__main__':
    voice_assistant = VoiceAssistant()
    voice_assistant.run()


# Próximos passos:
# Fazer uma função para passar a música ou voltar e pausar.
# Pensar na utilização do selenium para melhorar a abertura do spotify.
# Juntamente com o selenium, pensar em uma forma autônoma de clicar na página html