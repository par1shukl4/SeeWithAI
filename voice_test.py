

import speech_recognition as sr

recognizer = sr.Recognizer()

# Silence detection settings
recognizer.energy_threshold = 300       
recognizer.pause_threshold = 2.0        

print(" Speak: Ctrl+C to exit.")

try:
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("\n Listening...")
            audio = recognizer.listen(source)

        print(" Transcribing...")
        try:
            text = recognizer.recognize_google(audio)
            print(" You said:", text)
        except sr.UnknownValueError:
            print(" Could not understand audio.")
        except sr.RequestError as e:
            print(f" Could not request results; {e}")

except KeyboardInterrupt:
    print("\n Stopped by user.")