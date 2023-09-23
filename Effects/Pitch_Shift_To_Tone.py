#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 19:30:39 2023

@author: evana
"""

import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os
import math
import matplotlib.pyplot as plt


# Load the test audio file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
test_audio_file = os.path.join(parent_dir, 'IR_Files', 'test_5_seconds.wav')

test_audio, test_audio_rate = sf.read(test_audio_file)


# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time ')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(test_audio)) / test_audio_rate, test_audio)
plt.grid()
plt.show()






a_frequencies = [
    27.50,   # A0
    55.00,   # A1
    110.00,  # A2
    220.00,  # A3
    440.00,  # A4
    880.00,  # A5
    1760.00, # A6
    3520.00, # A7
    7040.00,  # A8
    14080.00 # A9
]



def calculate_frequency_ratio(target_frequency, original_frequency):
    return target_frequency / original_frequency

def PitchShiftToTone(signal, sample_rate, tune_frequencies):
    fft_result = np.fft.fft(signal)
    shifted_fft = np.zeros_like(fft_result)
    frequency_bins = [i * 0.2 for i in range(1,int(20000 / (1/(len(fft_result)/sample_rate))) + 1)]
    for i,bin_frequency in enumerate(frequency_bins):
        closest_target_frequency = min(tune_frequencies, key=lambda x: abs(x-bin_frequency))
        
        frequency_ratio = calculate_frequency_ratio(closest_target_frequency, bin_frequency)
        shifted_fft[i] = shifted_fft[i] + fft_result[i]*frequency_ratio
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    spacing = frequencies[1] #grabs second index to get spacing amount
    pitch_shifted_signal = np.real(np.fft.ifft(shifted_fft))
    return pitch_shifted_signal



pitch_shifted_audio = PitchShiftToTone(test_audio, test_audio_rate, a_frequencies)



frequencies = np.fft.fftfreq(len(np.fft.fft(test_audio)), 1 / test_audio_rate)

plt.figure(figsize=(12, 4))
plt.title('FFT of pitch shifted audio  (Magnitude Spectrum)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.plot(frequencies, np.fft.fft(pitch_shifted_audio) )
plt.grid()
plt.xlim(0, test_audio_rate / 2)  # Show only positive frequencies
plt.show()



# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time Pitch Shifted')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(pitch_shifted_audio)) / test_audio_rate, pitch_shifted_audio)
plt.grid()
plt.show()

sd.play(pitch_shifted_audio, test_audio_rate)
sd.wait()