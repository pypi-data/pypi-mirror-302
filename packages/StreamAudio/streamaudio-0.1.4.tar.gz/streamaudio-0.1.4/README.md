# StreamAI

**StreamAI** is a Python package designed for real-time audio streaming directly from the microphone. The audio is stored in memory, and the package provides a flexible way to handle or send the audio data to external applications or services in real time.

## Features
- Stream audio from the microphone directly into memory (without saving to disk).
- Handle audio data with a callback function to process it as needed (e.g., send to an API, analyze, etc.).
- Ideal for real-time applications such as voice-controlled systems or audio analysis.

## Installation

You can install **StreamAI** using pip:

```bash
pip install StreamAudio
```



## Example
```python
import pyaudio
import io
import threading
import time
import speech_recognition as sr

# Audio settings for streaming
FORMAT = pyaudio.paInt16  # Audio format: 16-bit resolution
CHANNELS = 1              # Mono channel
RATE = 16000              # Sample rate: 16kHz (common for speech)
CHUNK = 1024              # Buffer size per audio read
RECORD_SECONDS = 5        # Record only 5 seconds of audio

# Function to stream audio for a limited time and store it in memory
def stream_audio_to_memory(callback=None):
    """
    Streams audio from the microphone for 5 seconds, stores it in a BytesIO buffer in memory,
    and optionally passes the audio buffer to a callback function for processing.
    
    :param callback: Optional function to handle the in-memory audio data.
    """
    # Initialize PyAudio for audio streaming
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # BytesIO stream to hold audio data temporarily in memory
    audio_buffer = io.BytesIO()

    print("Recording audio for 5 seconds...")

    # Record for 5 seconds
    start_time = time.time()
    while time.time() - start_time < RECORD_SECONDS:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        audio_buffer.write(data)
    
    print("Recording complete.")

    # Clean up the stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Reset buffer pointer to the beginning
    audio_buffer.seek(0)

    # Show all recorded bytes
    print(f"Recorded bytes: {audio_buffer.getvalue()}")
    
    # If a callback function is provided, send the audio buffer for processing
    if callback:
        callback(audio_buffer)
    else:
        return audio_buffer

# Function to transcribe audio and print the result
def transcribe_audio(audio_buffer):
    """
    Transcribes audio from a BytesIO buffer using SpeechRecognition.
    
    :param audio_buffer: In-memory audio buffer to be transcribed.
    """
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Convert the BytesIO buffer into AudioData that speech_recognition can process
    audio_buffer.seek(0)  # Ensure we start reading from the beginning of the buffer
    audio_data = sr.AudioData(audio_buffer.read(), RATE, 2)

    try:
        # Perform the transcription using Google's speech recognition service
        text = recognizer.recognize_google(audio_data)
        print("Transcription:", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Function to start recording and processing audio
def start_audio_streaming():
    """
    Starts streaming audio from the microphone for 5 seconds,
    sends the recorded audio to be transcribed, and prints the bytes and transcription.
    """
    # Start streaming audio and transcribe after recording
    audio_buffer = stream_audio_to_memory(transcribe_audio)

# Start the recording and transcription
start_audio_streaming()
