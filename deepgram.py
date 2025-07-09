import websocket
import pyaudio
import threading
import json

# Deepgram API KEY (replace with your real key)
DEEPGRAM_API_KEY = "3ccc866db4aa253f99e8768fa1d8584b88679438"

RATE = 16000
CHUNK = 1024

class DeepgramSTT:
    def __init__(self):
        self.queue = Queue()
        self.ws = None

    def on_message(self, ws, message):
        data = json.loads(message)
        transcript = data.get("channel", {}).get("alternatives", [{}])[0].get("transcript", "")
        if transcript:
            self.queue.put(transcript)

    def on_error(self, ws, error):
        print("WebSocket Error:", error)

    def on_close(self, ws, *args):
        print("WebSocket Closed")

    def on_open(self, ws):
        print("🎤 Deepgram listening...")
        def run():
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
            while ws.keep_running:
                data = stream.read(CHUNK, exception_on_overflow=False)
                ws.send(data, websocket.ABNF.OPCODE_BINARY)
        threading.Thread(target=run, daemon=True).start()

    def start(self):
        deepgram_url = (
            f"wss://api.deepgram.com/v1/listen?sample_rate={RATE}&encoding=linear16&channels=1&punctuate=true"
        )
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        self.ws = websocket.WebSocketApp(
            deepgram_url,
            header=headers,
            on_open=self.on_open,
            on_+message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def get_transcript(self, timeout=20):
        try:
            transcript = self.queue.get(timeout=timeout)
            return transcript.strip().lower()
        except:
            return "Sorry, I didn't hear anything."