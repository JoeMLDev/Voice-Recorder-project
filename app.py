import tkinter as tk
import sounddevice as sd
import numpy as np
import wave

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.geometry("300x150")
        
        self.recording = False
        self.fs = 44100  # Sample rate
        self.audio_data = []

        # Add GUI elements
        self.label = tk.Label(self.root, text="Voice Recorder", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.save_button = tk.Button(self.root, text="Save Recording", command=self.save_recording, state=tk.DISABLED)
        self.save_button.pack(pady=5)
    
    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.audio_data = []  # Reset audio data
        self.record_audio()
    
    def stop_recording(self):
        self.recording = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
    
    def record_audio(self):
        if self.recording:
            audio_chunk = sd.rec(int(self.fs * 0.5), samplerate=self.fs, channels=2, dtype='int16')
            sd.wait()
            self.audio_data.append(audio_chunk)
            self.root.after(500, self.record_audio)  # Continue recording
    
    def save_recording(self):
        # Combine all recorded chunks into one array
        audio_array = np.concatenate(self.audio_data)
        
        # Save as WAV file
        with wave.open("output.wav", "wb") as wf:
            wf.setnchannels(2)  # Stereo
            wf.setsampwidth(2)  # 16-bit samples
            wf.setframerate(self.fs)
            wf.writeframes(audio_array.tobytes())
        
        self.save_button.config(state=tk.DISABLED)
        print("Recording saved as output.wav")

# Create the Tkinter window
root = tk.Tk()
app = VoiceRecorderApp(root)
root.mainloop()
