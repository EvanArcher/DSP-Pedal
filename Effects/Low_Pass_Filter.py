#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:20:35 2023

@author: pi
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



# Perform FFT and plot the magnitude spectrum
fft_result = np.fft.fft(test_audio)
magnitude_spectrum = np.abs(fft_result)
frequencies = np.fft.fftfreq(len(magnitude_spectrum), 1 / test_audio_rate)



# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time before low pass')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(test_audio)) / test_audio_rate, test_audio)
plt.grid()
plt.show()



plt.figure(figsize=(12, 4))
plt.title('FFT (Magnitude Spectrum)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.plot(frequencies, fft_result)
plt.grid()
plt.xlim(0, test_audio_rate / 2)  # Show only positive frequencies
plt.show()

low_pass_output_fft=fft_result
low_pass_output_fft[5000:-1] = 0 # set higher frequencies to zero

plt.figure(figsize=(12, 4))
plt.title('FFT Low Pass(Magnitude Spectrum)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.plot(frequencies, low_pass_output_fft)
plt.grid()
plt.xlim(0, test_audio_rate / 2)  # Show only positive frequencies
plt.show()

low_pass_audio = np.real(np.fft.ifft(low_pass_output_fft))

# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time low pass')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(low_pass_audio)) / test_audio_rate, low_pass_audio)
plt.grid()
plt.show()


sd.play(test_audio, test_audio_rate)
sd.wait()  # Wait until the sound is finished playing
sd.play(low_pass_audio, test_audio_rate)
sd.wait()