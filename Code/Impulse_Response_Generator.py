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

# Load impulse audio file
impulse_file_path = 'Fender_Twin_Reverb.wav'
impulse_signal, impulse_sr = sf.read(impulse_file_path)
try:
    if impulse_signal.shape[1] == 2: # check if impulse is dual signal
        impulse_signal = np.mean(impulse_signal, axis=1)
except:
    None
audio_file_path = "test_5_seconds.wav"
audio_signal, sample_rate = sf.read(audio_file_path)
clean_audio = audio_signal
# Normalize impulse to peak amplitude of 1


#start_time = time.time()
#normalized_impulse = impulse_signal / np.max(np.abs(impulse_signal))
#
## Determine desired impulse response length (same as audio signal length)
#desired_length = len(audio_signal)
#
## Pad or trim the impulse to match desired length
#impulse_response = normalized_impulse[:desired_length]
#
## Perform convolution and apply the filter
#filtered_audio = np.convolve(audio_signal, impulse_response, mode='same')
#end_time = time.time()
#print('Convolution total time is : ', end_time-start_time)
#sd.play(clean_audio, sample_rate)
#sd.wait()  # Wait until the sound is finished playing
#sd.play(filtered_audio, sample_rate)
#sd.wait()


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
sd.play(clean_audio, sample_rate)
sd.wait()  # Wait until the sound is finished playing
sd.play(convolved_signal, sample_rate)
sd.wait()