import pyaudio
import io
import threading

# Audio settings for streaming
FORMAT = pyaudio.paInt16  # Audio format: 16-bit resolution
CHANNELS = 1              # Mono channel
RATE = 16000              # Sample rate: 16kHz (common for speech)
CHUNK = 1024              # Buffer size per audio read

# Function to stream audio and store it in memory
def stream_audio_to_memory(callback=None, stop_event=None):
    """
    Streams audio from the microphone, stores it in a BytesIO buffer in memory,
    and optionally passes the audio buffer to a callback function for processing.

    :param callback: Optional function to handle the in-memory audio data.
    :param stop_event: Optional threading.Event() to stop the stream.
    """
    # Initialize PyAudio for audio streaming
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # BytesIO stream to hold audio data temporarily in memory
    audio_buffer = io.BytesIO()

    print("Recording audio... Press Ctrl+C to stop.")

    try:
        while True:
            if stop_event and stop_event.is_set():
                break

            # Read audio data from the stream
            data = stream.read(CHUNK)
            audio_buffer.write(data)

            # If a callback function is provided, send the audio buffer for processing
            if callback:
                callback(audio_buffer)
                audio_buffer.seek(0)  # Reset buffer pointer for the next read
                audio_buffer.truncate(0)  # Clear the buffer after processing if necessary
    except KeyboardInterrupt:
        print("Recording stopped by user.")
    finally:
        # Clean up the stream and PyAudio instance
        stream.stop_stream()
        stream.close()
        audio.terminate()

    audio_buffer.seek(0)  # Reset buffer pointer to the beginning
    return audio_buffer

# Start audio streaming in a separate thread
def start_audio_streaming(callback=None):
    """
    Starts streaming audio from the microphone in a separate thread.

    :param callback: Optional function to handle the audio data in real time.
    :return: threading.Event() object to control stopping the thread.
    """
    stop_event = threading.Event()  # Event to signal stopping the stream

    # Start streaming audio in a thread without blocking the main program
    audio_thread = threading.Thread(target=stream_audio_to_memory, args=(callback, stop_event))
    audio_thread.start()

    # Return the stop_event to allow stopping the thread externally
    return stop_event

# Example function to demonstrate how to handle the in-memory stream
def handle_audio_stream(callback=None):
    """
    Handles the audio stream by starting the audio streaming process
    and passing the in-memory audio data to a callback for further processing.

    :param callback: Function to process the audio stream.
    :return: threading.Event() object to control stopping the stream externally.
    """
    return start_audio_streaming(callback)
