#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 17:06:54 2023

@author: pi
"""

import numpy as np
import soundfile as sf
import sounddevice as sd
import time 
import os
import matplotlib.pyplot as plt


# Load impulse audio file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

file_path = os.path.join(parent_dir, 'IR_Files', 'r1_omni.wav')

impulse_file_path = file_path
impulse_signal, impulse_sr = sf.read(impulse_file_path)
try:
    if impulse_signal.shape[1] == 2: # check if impulse is dual signal
        impulse_signal = np.mean(impulse_signal, axis=1)
except:
    None
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

file_path = os.path.join(parent_dir, 'IR_Files', 'test_5_seconds.wav')
audio_file_path = file_path
audio_signal, sample_rate = sf.read(audio_file_path)
clean_audio = audio_signal

impulse_abs = abs(impulse_signal)
noise_threshold = 10**(-2)

# Find the indices where the audio signal exceeds the noise threshold
above_threshold_indices = np.where(impulse_abs > noise_threshold)[0]

if len(above_threshold_indices) > 0:
    start_index = above_threshold_indices[0]
    end_index = above_threshold_indices[-1]
else:
    # If no non-silent sections found, handle this case accordingly
    start_index = 0
    end_index = 0

# Extract and concatenate the non-silent sections
non_silent_sections = impulse_signal[start_index:end_index + 1]


plt.plot(impulse_signal)

# Add labels and a title
plt.xlabel("data points")
plt.ylabel("Y-axis Label")
plt.title("impulse")

# Display the plot
plt.show()


plt.plot(non_silent_sections)

plt.xlabel("data points")
plt.ylabel("Y-label")
plt.title("impulse adjusted")
plt.show()

#%% FFT method

# Normalize impulse to peak amplitude of 1
start_time = time.time()
normalized_impulse = impulse_signal / np.max(np.abs(impulse_signal))

# Determine desired impulse response length (same as audio signal length)
desired_length = len(audio_signal)
padded_impulse = np.pad(normalized_impulse,(0, desired_length - len(normalized_impulse)))
# Pad or trim the impulse to match desired length

fft_audio = np.fft.fft(audio_signal)
fft_impulse = np.fft.fft(padded_impulse)

convolved_fft = fft_audio * fft_impulse

convolved_signal = np.real(np.fft.ifft(convolved_fft))

# Perform convolution and apply the filter

end_time = time.time()
print('Convolution using fft total time is : ', end_time-start_time)
# sd.play(clean_audio, sample_rate)
# sd.wait()  # Wait until the sound is finished playing
# sd.play(convolved_signal, sample_rate)
# sd.wait()