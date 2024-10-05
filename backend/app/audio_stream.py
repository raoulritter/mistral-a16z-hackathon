import pyaudio
import numpy as np
import tkinter as tk

class AudioStreamer:
    def __init__(self, callback):
        self.callback = callback
        self.is_recording = False
        self.frames = []
        self.sample_rate = 16000
        self.chunk_size = 1024

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.setup_gui()

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.title("Audio Streamer")
        self.button = tk.Button(self.window, text="Start Recording", command=self.toggle_recording)
        self.button.pack()

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.button.config(text="Stop Recording")
        self.frames = []
        try:
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size)
            self.stream_audio()
        except Exception as e:
            print(f"Error starting audio stream: {e}")
            self.is_recording = False
            self.button.config(text="Start Recording")

    def stop_recording(self):
        self.is_recording = False
        self.button.config(text="Start Recording")
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        audio_data = np.frombuffer(b''.join(self.frames), dtype=np.int16)
        self.callback(audio_data)

    def stream_audio(self):
        if self.is_recording and self.stream:
            try:
                data = self.stream.read(self.chunk_size)
                self.frames.append(data)
                self.window.after(10, self.stream_audio)
            except Exception as e:
                print(f"Error reading audio stream: {e}")
                self.stop_recording()

    def run(self):
        self.window.mainloop()

    def __del__(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()