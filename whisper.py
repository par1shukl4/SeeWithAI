import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fix OpenMP DLL conflict on Windows

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Load the model from local path (downloaded repo)
model_dir = "faster-whisper-small"  # your cloned repo folder name
model = WhisperModel(model_dir, local_files_only=True)

# Settings
samplerate = 16000
duration = 5  # seconds for each chunk

def callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    audio = indata[:, 0]
    print("🔊 Transcribing...")

    audio = np.array(audio, dtype=np.float32)
    segments, _ = model.transcribe(audio, vad_filter=True, beam_size=5)
    for segment in segments:
        print("🗣️ You said:", segment.text.strip())

print("🎤 Speak now (press Ctrl+C to stop)...")

try:
    with sd.InputStream(callback=callback, channels=1, samplerate=samplerate, blocksize=int(samplerate * duration)):
        while True:
            sd.sleep(1000)
except KeyboardInterrupt:
    print("\n🛑 Stopped.")
