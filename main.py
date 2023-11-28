import speech_recognition as sr
import requests
import json
import pyttsx3

def get_user_speech(engine):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        engine.say("Please say the name of the city.")
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source)
            text = recognizer.recognize_google(audio_data)
            engine.say(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            engine.say("Sorry, I couldn't understand the speech.")
            return None

def get_weather(city):
    api_key = "UOPjdsE3mN5i2mBHzAhvFxHqX1hIkN99"
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={api_key}"
    r = requests.get(url)
    result_data = r.json()

    try:
        temp = result_data["data"]["timelines"][0]["intervals"][0]["values"]["temperature"]
    except KeyError:
        print("KeyError: 'temperature' not found in the response")
        temp = None

    return temp

def main():
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)

    city = get_user_speech(engine)

    if city:
        temperature = get_weather(city)

        if temperature is not None:
            result = f"The temperature in {city} is {temperature}."
            print(result)

            engine.say(result)
            engine.runAndWait()
        else:
            engine.say("Unable to fetch temperature.")

if __name__ == "__main__":
    main()
