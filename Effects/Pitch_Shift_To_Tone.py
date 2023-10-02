#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 19:30:39 2023

@author: evana
"""

import sounddevice as sd
import numpy as np
import soundfile as sf
import os
import matplotlib.pyplot as plt

# Load the test audio file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
test_audio_file = os.path.join(parent_dir, 'IR_Files', 'test_5_seconds.wav')
test_audio, test_audio_rate = sf.read(test_audio_file)

# Define parameters for framing
FRAME_SIZE = 2048  # Define the size of each frame
HOP_SIZE = int(FRAME_SIZE * .01)  # Define the hop size (overlap between frames)
NUM_FRAMES = int((len(test_audio) - FRAME_SIZE) / HOP_SIZE) + 1  # Calculate the total number of frames

# Plot the original audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time ')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(test_audio)) / test_audio_rate, test_audio)
plt.grid()



    
# Define target frequencies (A notes) for auto-tuning
a_frequencies = [
    27.50, 55.00, 110.00, 220.00, 440.00,
    880.00, 1760.00, 3520.00, 7040.00, 14080.00
]

def find_dominant_frequencies(fft_magnitude, threshold=0.5):
    """
    Find dominant frequencies in the signal using a threshold-based approach.
    """
    max_magnitude = np.max(fft_magnitude)
    dominant_indices = np.where(fft_magnitude > max_magnitude * threshold)[0]
    return dominant_indices

def PitchShiftToTone(signal, sample_rate, tune_frequencies):
    """
    Perform pitch shifting of the signal towards target frequencies.
    """
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    magnitude = np.abs(fft_result)
    phase = np.angle(fft_result)
    dominant_indices = find_dominant_frequencies(magnitude)

    for i in dominant_indices:
        freq = abs(frequencies[i])
        closest_target_frequency = min(tune_frequencies, key=lambda x: abs(x-freq))
        shift_amount = int((closest_target_frequency - freq) / (sample_rate/len(signal)))

        # Shift the dominant frequencies to target frequencies
        if i + shift_amount < len(fft_result) and i + shift_amount >= 0:  # Bound check
            fft_result[i + shift_amount] = magnitude[i] * np.exp(1j * phase[i])
            fft_result[i] = 0
    return np.real(np.fft.ifft(fft_result))


# Frame the signal into overlapping frames
frames = np.array([test_audio[i:i + FRAME_SIZE] for i in range(0, len(test_audio) - FRAME_SIZE + 1, HOP_SIZE)])
pitch_shifted_frames = [PitchShiftToTone(frame, test_audio_rate, a_frequencies) for frame in frames]

# Reconstruct the signal using the overlap-add method
pitch_shifted_audio = np.zeros(len(test_audio))
for n, frame in enumerate(pitch_shifted_frames):
    start = n * HOP_SIZE
    end = start + FRAME_SIZE
    pitch_shifted_audio[start:end] += frame

# Plot FFT of the pitch-shifted audio signal
frequencies = np.fft.fftfreq(len(np.fft.fft(test_audio)), 1 / test_audio_rate)
plt.figure(figsize=(12, 4))
plt.title('FFT of Pitch Shifted Audio (Magnitude Spectrum)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.plot(frequencies, np.abs(np.fft.fft(pitch_shifted_audio)))  # Use absolute value for magnitude
plt.grid()
plt.xlim(0, test_audio_rate / 2)

# Plot the pitch-shifted audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time Pitch Shifted')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(pitch_shifted_audio)) / test_audio_rate, pitch_shifted_audio)
plt.grid()
plt.show()

# Play the pitch-shifted audio
# sd.play(pitch_shifted_audio, test_audio_rate)
# sd.wait()