#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 18:00:15 2023

@author: evana
"""


import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os



class LiveAudio:
    def __init__(self, IR_Data, IR_Rate): #input IR and Rate
        self.IR_Data = IR_Data
        self.IR_Rate = IR_Rate
        
    def PlaySound(self):
        samp_rate = 96000 # 192kHz sampling rate
        chunk = 4800*3  # 100ms of data at 192kHz
        dev_index = 2  # device index
        
        # Resample IR based on our sample rate
        if samp_rate != self.IR_Rate:
            num_samples = int(len(self.IR_Data) * samp_rate / self.IR_Rate)
            ir_resampled = resample(self.IR_Data, num_samples)
        else:
            ir_resampled = self.IR_Data

        # Partition the impulse response
        num_partitions = int(np.ceil(len(ir_resampled) / chunk))
        ir_partitions = [ir_resampled[i*chunk:(i+1)*chunk] for i in range(num_partitions)]


        # FFT of each partition, zero-padded to 2*chunk
        IR_ffts = [np.fft.fft(np.pad(part, (0, 2*chunk - len(part)))) for part in ir_partitions]


        # To store the tails of the convolution results
        tails = [np.zeros(chunk) for _ in range(num_partitions)]

        # Callback function to handle streaming
        def callback(indata, outdata, frames, time, status):
            global tails
            if status:
                print(status)
            
            # Ensure indata is a 1D array
            indata = indata.flatten()

            # Zero-pad the input data and compute its FFT
            indata_fft = np.fft.fft(np.pad(indata, (0, chunk)))
            
            # Initialize the output signal as zeros
            output_signal = np.zeros(chunk)
            
            # Convolve with each partition and sum the results
            for i, IR_fft in enumerate(IR_ffts):
                convolved_fft = indata_fft * IR_fft
                segment = np.real(np.fft.ifft(convolved_fft))
                
                # Add the current segment and its tail from the previous frame to the output_signal
                output_signal += segment[:chunk] + tails[i]
                
                # Store the tail for the next chunk
                tails[i] = segment[chunk:2*chunk]
            
            # Send the summed convolution to the output
            outdata[:] = output_signal.reshape(-1, 1)


            
        with sd.Stream(samplerate=samp_rate, blocksize=chunk, device=dev_index, channels=1, callback=callback):
            print("Press Enter to stop streaming...")
            input()

        print("Streaming terminated.")




