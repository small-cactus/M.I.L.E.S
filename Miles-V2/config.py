import openwakeword
from openwakeword.model import Model
import speech_recognition as sr
import whisper
import time
from urllib3.exceptions import NotOpenSSLWarning
import warnings

# Suppress the specific FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Suppress the specific NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning, message=".*OpenSSL 1.1.1+.*")
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
warnings.filterwarnings("ignore")




# One-time download of all pre-trained models (or only select models)
print("[Miles is Downloading wake word model...]")
openwakeword.utils.download_models()
print("[Miles is Wake word models downloaded...]")

# Additionally, ensure the whisper models are downloaded
time.sleep(2)
print("[Miles is Downloading speech recognition models...]")
whisper.load_model("base")
print("[Miles is Base model downloaded successfully...]")
time.sleep(2)
print("[Miles is Downloading tiny model...]")
whisper.load_model("tiny")
print("[Miles is Tiny model downloaded successfully...]")
time.sleep(2)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Miles is Ready for speech, try saying 'this is a test']")
        audio = r.listen(source)  # Listen until silence is detected

    # Save the captured audio to a WAV file
    audio_file = "captured_audio.wav"
    with open(audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    try:
        # Load the Whisper model
        model = whisper.load_model("base")  # Start with the base model
        start_time = time.time()  # Record the start time
        result = model.transcribe(audio_file)
        end_time = time.time()  # Record the end time

        # Check if the transcription took longer than 3 seconds
        if end_time - start_time > 3:
            raise TimeoutError("Transcription took longer than 3 seconds with the base model.")

    except (Exception, TimeoutError) as e:
        print(f"Switching to tiny model due to: {str(e)}")
        model = whisper.load_model("tiny")  # Fallback to the tiny model
        result = model.transcribe(audio_file)

    return result["text"]



if __name__ == "__main__":
    text = listen()
    print(f"[Miles is You said: {text}]")
    time.sleep(2)
    print("[Miles is Config Complete!]")


