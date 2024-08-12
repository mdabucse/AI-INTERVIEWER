import sounddevice as sd
import wavio
import numpy as np
import threading
import keyboard  


def record_audio(filename, fs=44100):
    global recording, audio_data
    audio_data = np.empty((0, 1), dtype='int16')  # Initialize empty array to store audio
    recording = True
    print("Recording... Press 's' to stop.")
    
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


def record():
    # Parameters
    filename = "output.wav"  # Output file name

    # Start recording in a separate thread
    recording_thread = threading.Thread(target=record_audio, args=(filename,))
    recording_thread.start()
    
    # Wait for the user to press 's' to stop the recording
    keyboard.wait('s')
    global recording
    recording = False
    recording_thread.join()


def Capture():
    print("Press 'r' to start recording.")
    keyboard.wait('r')  # Wait until 'r' is pressed to start recording
    record()
