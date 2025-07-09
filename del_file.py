

"""import json
import csv
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import edge_tts
import subprocess
import speech_recognition as sr

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# === TEXT TO SPEECH USING EDGE-TTS AND FFMPEG ===
async def speak(text):
    filename = "voice_output.mp3"
    communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await communicate.save(filename)

    subprocess.run([
        r"C:\\Users\\Nitya Nand\\Desktop\\office\\chatterbot\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffplay.exe",
        "-nodisp", "-autoexit", filename
    ])

# === VOICE INPUT ===
def listen():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2.0
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            transcript = recognizer.recognize_google(audio).strip().lower()
            if transcript in ["bye", "exit", "quit"]:
                os._exit(0)  # Immediately exit the process
            return transcript
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech service error."

# === LOAD INTENTS ===
with open('intents.json', 'r') as f:
    intents = json.load(f)
required_questions = [q["question"] for q in intents["intents"]]
asked_questions = set()

# === SYSTEM PROMPT ===
system_prompt = (
    "You are an exit interview bot. You must conduct a polite, natural conversation. "
    "If the user seems confused, rephrase or repeat the question. Only move on when the question has been answered clearly. "
    "Ensure that all the following questions are eventually covered (but not all at once). Ask them naturally when the moment fits.\n\n"
    + "\n".join(f"- {q}" for q in required_questions)
)

# === START CHAT SESSION ===
chat = model.start_chat(history=[
    {"role": "user", "parts": [system_prompt]}
])

# === COLLECT BASIC USER INFO ===
print("\nWelcome to the Exit Interview Bot\nPlease answer a few questions before we begin:\n")

user_info = {
    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'Name': input("What is your full name?\nYou: "),
    'Department': input("Which department are you from?\nYou: "),
    'Job Title': input("What was your job title?\nYou: "),
    'Years Worked': input("How many years did you work here?\nYou: ")
}

print("\nThank you! Let's begin your exit interview. Type 'bye' anytime to exit.\n")

# === CREATE CSV ===
csv_file = 'interview_responses.csv'
is_new_file = not os.path.exists(csv_file)

with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    if is_new_file:
        writer.writerow(["No.", "Question", "Answer"])

    writer.writerow([])
    writer.writerow(["--- Exit Interview ---"])
    for key, value in user_info.items():
        writer.writerow([key, value])
    writer.writerow([])

    count = 1  # Question numbering

    # === DYNAMIC CHAT LOOP ===
    while True:
        remaining = [q for q in required_questions if q not in asked_questions]

        if remaining:
            guidance = "\nContinue the conversation. Make it feel natural. Use any of these remaining questions when appropriate:\n" + "\n".join(f"- {q}" for q in remaining[:2])
        else:
            guidance = "\nAll required questions have been covered. You may now thank the user and end politely."

        response = chat.send_message("Continue the conversation." + guidance)
        bot_message = response.text.strip()

        print(f"Bot: {bot_message}")
        asyncio.run(speak(bot_message))

        while True:
            user_input = listen()
            print("You:", user_input)

            unclear_phrases = ["not sure", "maybe", "idk", "don't know", "unsure", "repeat", "again", "what do you mean", "unclear", "confused"]
            clear_yes_no = ["yes", "no", "yeah", "nope", "yep", "nah"]
            user_clean = user_input.strip().lower()

            if (
                user_clean not in clear_yes_no and
                (any(p in user_clean for p in unclear_phrases) or len(user_clean) < 5)
            ):
                follow_up_prompt = f"The user said: '{user_input}'. Please rephrase or clarify the previous question."
                follow_up = chat.send_message(follow_up_prompt)
                follow_up_msg = follow_up.text.strip()
                print("Bot (clarified):", follow_up_msg)
                asyncio.run(speak(follow_up_msg))
                continue  # ask for input again instead of moving on

            writer.writerow([count, bot_message, user_input])
            count += 1
            chat.send_message(user_input)

            for q in remaining:
                if q.lower() in bot_message.lower():
                    asked_questions.add(q)
                    break

            break

    final_msg = "Interview complete. Thank you for your time!"
    print("\n" + final_msg)
    asyncio.run(speak(final_msg))
"""