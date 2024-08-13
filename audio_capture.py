import sounddevice as sd
import wavio
import numpy as np
import threading

# Global variables to manage recording state
recording = False
audio_data = np.empty((0, 1), dtype='int16')

def record_audio(filename, fs=44100):
    global recording, audio_data
    audio_data = np.empty((0, 1), dtype='int16')  # Initialize empty array to store audio
    recording = True
    print("Recording...")

    def callback(indata, frames, time, status):
        if recording:
            global audio_data
            audio_data = np.append(audio_data, indata)
        else:
            raise sd.CallbackStop

    with sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback):
        while recording:
            sd.sleep(100)

    # Save the audio as a .wav file
    wavio.write(filename, audio_data, fs, sampwidth=2)
    print(f"Audio saved as {filename}")

def start_recording(filename):
    global recording
    recording = True
    recording_thread = threading.Thread(target=record_audio, args=(filename,))
    recording_thread.start()
    return recording_thread

def stop_recording():
    global recording
    recording = False
