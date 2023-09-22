#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 20:22:53 2023

@author: Evan Archer
"""

import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os
import matplotlib.pyplot as plt


# Load the test audio file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
test_audio_file = os.path.join(parent_dir, 'IR_Files', 'test_5_seconds.wav')

test_audio, test_audio_rate = sf.read(test_audio_file)

# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(test_audio)) / test_audio_rate, test_audio)
plt.grid()
plt.show()









# Perform FFT and plot the magnitude spectrum
fft_result = np.fft.fft(test_audio)
magnitude_spectrum = np.abs(fft_result)
frequencies = np.fft.fftfreq(len(magnitude_spectrum), 1 / test_audio_rate)

plt.figure(figsize=(12, 4))
plt.title('FFT (Magnitude Spectrum)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.plot(frequencies, magnitude_spectrum)
plt.grid()
plt.xlim(0, test_audio_rate / 2)  # Show only positive frequencies
plt.show()





# Define the pitch shift factor (e.g., 1.5 for a 1.5x pitch shift)
pitch_shift_factor = 1.5

# Perform FFT
fft_result = np.fft.fft(test_audio)

# Calculate the new number of bins for pitch shifting
shifted_length = int(len(test_audio) * pitch_shift_factor)
shifted_fft_result = np.zeros(shifted_length, dtype=np.complex128)

# Shift the FFT bins to perform pitch shifting
for i in range(shifted_length):
    orig_idx = int(i / pitch_shift_factor)
    if orig_idx < len(fft_result):
        shifted_fft_result[i] = fft_result[orig_idx]



magnitude_spectrum = np.abs(shifted_fft_result)
frequencies = np.fft.fftfreq(len(magnitude_spectrum), 1 / test_audio_rate)
plt.figure(figsize=(12, 4))
plt.title('FFT Shifted (Magnitude Spectrum)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.plot(frequencies, magnitude_spectrum)
plt.grid()
plt.xlim(0, test_audio_rate / 2)  # Show only positive frequencies
plt.show()

# Perform iFFT to obtain the pitch-shifted audio
shifted_audio = np.fft.ifft(shifted_fft_result).real

# Plot the pitch-shifted audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Pitch-Shifted Audio Signal Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(shifted_audio)) / test_audio_rate, shifted_audio)
plt.grid()
plt.show()

# Save the pitch-shifted audio to a file (optional)
sf.write('pitch_shifted_audio.wav', shifted_audio, test_audio_rate)


audio, sample_rate = sf.read(test_audio_file)

# Define the target pitch (e.g., 1.5 for a 1.5x lower pitch)
target_pitch = 1.5

# Calculate the resampling factor to achieve the desired pitch change
resampling_factor = 1 / target_pitch

# Resample the audio to lower the pitch while maintaining duration
pitch_shifted_audio = resample(audio, int(len(audio) * resampling_factor))

# Save the pitch-shifted audio to a file (optional)
sf.write('pitch_shifted_audio_same_length.wav', pitch_shifted_audio, sample_rate)