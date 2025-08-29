import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import music
# from openai import OpenAI 

re = sr.Recognizer()
engine = pyttsx3.init()



def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def query_gemini(prompt):
    api_key = "AIzaSyAYDhe-7IyJDhNO8Ft2p5nFuIpRgmCx6rU"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        responce = requests.post(url, headers=headers, json=payload)
        responce.raise_for_status()
        # Extract the response text from the JSON
        return responce.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Sorry, an error occurred: {e}"

    
def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        print("The google is open!")
        speak("Google opened!") 
        
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com") 
        print("the Youtube is open")
        speak("youtube opened!") 
         
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        print("the linkedin is opened")
        speak("linkedin opened!") 
        
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        print("the facebbok is opened")
        speak("facebook opened!") 
        
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split(" ")[1]
            link = music.music[song]
            webbrowser.open(link)
        
        except Exception as e:  
            print(f"cant run:{e}")
    else:
        try:
            responce = query_gemini(c)
            speak(responce)
        except Exception as e:
            print(f"exception as:{e}")
    
        
if __name__ == "__main__":
    speak("Jarvis AI Assistant Activated")
    print("System Ready. Say 'Jarvis' to activate.")
    while True:
        
        print("recognizing....")
        
        try:
            with sr.Microphone() as source:
                print("Listening.....")
                re.adjust_for_ambient_noise(source)
                audio = re.listen(source, timeout=5,phrase_time_limit=5)
            word = re.recognize_google(audio)
            if "jarvis" in word.lower():
                speak("Ya")
                
                with sr.Microphone() as source:
                    print("jarvis active.....")
                    audio = re.listen(source, timeout=8,phrase_time_limit=8)
                cmd = re.recognize_google(audio)
                 
                processcommand(cmd) 
            
            elif "stop" in word.lower():
                print("Thanks!")
                print("Exit!r")
                speak("Goodbye!") 
                break
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:

            print(e)  

