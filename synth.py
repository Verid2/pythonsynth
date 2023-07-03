import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment
from pydub.playback import play

# Synthesizer parameters
duration = 1000  # Duration of each note in milliseconds
frame_rate = 44100  # Sample rate

# Function to generate a waveform of a given type, frequency, and octave
def generate_waveform(wave_type, frequency):
    t = np.linspace(0, duration / 1000, int(frame_rate * duration / 1000), False)

    if wave_type == 'Sine':
        wave = np.sin(2 * np.pi * frequency * t)
    elif wave_type == 'Square':
        wave = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == 'Sawtooth':
        wave = (2 * frequency * t) % 2 - 1
    else:
        return None

    return (wave * 32767).astype(np.int16)

# Function to play a piano key of a given frequency and wave type
def play_piano_key(frequency, wave_type):
    # Generate the waveform
    waveform = generate_waveform(wave_type, frequency)
    if waveform is None:
        return

    # Create an audio segment from the waveform
    audio = AudioSegment(waveform.tobytes(), frame_rate=frame_rate, sample_width=waveform.dtype.itemsize, channels=1)

    # Play the audio segment
    play(audio)

    # Update the oscilloscope plot
    t = np.linspace(0, duration / 1000, len(waveform), endpoint=False)
    line.set_data(t, waveform)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

# Create the main window
window = tk.Tk()
window.title("Piano Synthesizer")

# Create a wave type selection variable
wave_type_var = tk.StringVar()
wave_type_var.set('Sine')

# Create piano keys frame
piano_keys_frame = tk.Frame(window)
piano_keys_frame.pack()

# Define piano key frequencies and text labels
piano_keys = [
    {'text': 'C', 'frequency': 261.63},
    {'text': 'D', 'frequency': 293.66},
    {'text': 'E', 'frequency': 329.63},
    {'text': 'F', 'frequency': 349.23},
    {'text': 'G', 'frequency': 392.00},
    {'text': 'A', 'frequency': 440.00},
    {'text': 'B', 'frequency': 493.88}
]

# Create piano keys buttons
for key in piano_keys:
    button = tk.Button(piano_keys_frame, text=key['text'], command=lambda f=key['frequency'], wt=wave_type_var.get(): play_piano_key(f, wt))
    button.pack(side=tk.LEFT, padx=2, pady=2)

# Create a wave type selection dropdown
wave_type_label = tk.Label(window, text="Wave Type:")
wave_type_label.pack()
wave_type_dropdown = tk.OptionMenu(window, wave_type_var, 'Sine', 'Square', 'Sawtooth')
wave_type_dropdown.pack()

# Create the oscilloscope plot
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(0, duration / 1000)
ax.set_ylim(-32768, 32767)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
line, = ax.plot([], [], color='blue')  # Set the line color explicitly
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

# Start the GUI event loop
window.mainloop()
