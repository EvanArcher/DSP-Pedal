#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:20:35 2023

@author: Evan Archer
"""

import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os
import matplotlib.pyplot as plt
import math


# Load the test audio file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
test_audio_file = os.path.join(parent_dir, 'IR_Files', 'test_5_seconds.wav')

test_audio, test_audio_rate = sf.read(test_audio_file)


#input the signal, sample rate, and cutoff frequency and 
# get the low pass audio out
def LowPassFilter(signal, sample_rate, cutoff):
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    spacing = frequencies[1] #grabs second index to get spacing amount
    cutoff_index = math.ceil(cutoff/spacing)
    fft_result[cutoff_index:-1] = 0
    low_pass_signal = np.real(np.fft.ifft(fft_result))
    return low_pass_signal
    

def HighPassFilter(signal, sample_rate, cutoff):
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    spacing = frequencies[1] #grabs second index to get spacing amount
    cutoff_index = math.ceil(cutoff/spacing)
    fft_result[0:cutoff_index] = 0
    high_pass_signal = np.real(np.fft.ifft(fft_result))
    return high_pass_signal

def BandPassFilter(signal, sample_rate, lowcutoff,highcutoff):
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    spacing = frequencies[1] #grabs second index to get spacing amount
    lowcutoff_index = math.ceil(lowcutoff/spacing)
    highcutoff_index = math.ceil(highcutoff/spacing)
    fft_result[0:lowcutoff_index] = 0
    fft_result[highcutoff_index:-1] = 0
    band_pass_signal = np.real(np.fft.ifft(fft_result))
    return band_pass_signal

def BassBooster(signal, sample_rate, cutoff, boost_amount):
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    spacing = frequencies[1] #grabs second index to get spacing amount
    cutoff_index = math.ceil(cutoff/spacing)
    fft_result[0:cutoff_index] = fft_result[0:cutoff_index]*boost_amount
    bass_boosted_signal = np.real(np.fft.ifft(fft_result))
    return bass_boosted_signal


low_pass_audio = LowPassFilter(test_audio, test_audio_rate, 1000)
high_pass_audio = HighPassFilter(test_audio, test_audio_rate, 10000)
band_pass_audio = BandPassFilter(test_audio, test_audio_rate, 2000, 10000)
bass_boosted_audio = BassBooster(test_audio, test_audio_rate, 1000, 50)

# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time ')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(test_audio)) / test_audio_rate, test_audio)
plt.grid()
plt.show()

# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time low pass')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(low_pass_audio)) / test_audio_rate, low_pass_audio)
plt.grid()
plt.show()

# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time high pass')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(high_pass_audio)) / test_audio_rate, high_pass_audio)
plt.grid()
plt.show()

# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time band pass')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(band_pass_audio)) / test_audio_rate, band_pass_audio)
plt.grid()
plt.show()

# Plot the audio signal over time
plt.figure(figsize=(12, 4))
plt.title('Audio Signal Over Time Bass boosted')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(np.arange(len(bass_boosted_audio)) / test_audio_rate, bass_boosted_audio)
plt.grid()
plt.show()


# sd.play(test_audio, test_audio_rate)
# sd.wait()  # Wait until the sound is finished playing
# sd.play(low_pass_audio, test_audio_rate)
# sd.wait()
# sd.play(high_pass_audio, test_audio_rate)
# sd.wait()
# sd.play(band_pass_audio, test_audio_rate)
# sd.wait()
# sd.play(bass_boosted_audio, test_audio_rate)
# sd.wait()