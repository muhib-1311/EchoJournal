import os
import wave
import pyaudio
import speech_recognition as sr
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Load API key
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Recording settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
TEMP_WAV = "temp_recording.wav"

def record_audio_manually():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    print("🎙️ Press ENTER to start recording...")
    input()
    print("🔴 Recording... Press ENTER again to stop.")
    
    frames = []
    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if os.name == 'nt':
                import msvcrt
                if msvcrt.kbhit():
                    if msvcrt.getch() == b'\r':  # ENTER key
                        break
            else:
                # For Mac/Linux, stop using Ctrl+C or modify to accept input
                pass
    except KeyboardInterrupt:
        print("\n⏹️ Recording stopped by Ctrl+C.")
    
    print("⏹️ Done. Saving audio...")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(TEMP_WAV, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return TEMP_WAV


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        print("📝 You said:\n", text)
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand.")
        return None
    except sr.RequestError as e:
        print("❌ Speech API error:", e)
        return None


def summarize_text(text):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that rewrites journal entries into clear, first-person summaries. Respond as if the user is writing the summary themselves, and do not explain what the entry is about. Start directly with the summary in first person. Avoid phrases like 'the journal entry says...'"
                },
                {
                    "role": "user",
                    "content":  f"Rewrite this journal entry as a clear, personal summary in first person:\n\n{text}"
                }
            ]
        )
        summary = response.choices[0].message.content.strip()
        print("📄 Summary:\n", summary)
        return summary
    except Exception as e:
        print("❌ Groq API error:", e)
        return "Summary not available."


def save_to_journal(summary):
    journal_dir = os.path.join(os.path.dirname(__file__), "journal_entries")
    os.makedirs(journal_dir, exist_ok=True)

    filename = os.path.join(journal_dir, f"{datetime.now().strftime('%Y-%m-%d')}.txt")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(summary + "\n\n")
    print(f"✅ Saved to {filename}")


# Run
if __name__ == "__main__":
    audio_file = record_audio_manually()
    spoken_text = transcribe_audio(audio_file)
    if spoken_text:
        summary = summarize_text(spoken_text)
        save_to_journal(summary)
    else:
        print("⚠️ No usable speech detected.")
