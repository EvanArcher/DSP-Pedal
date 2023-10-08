#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 17:27:10 2023

@author: pi
"""

#This class is designed to take as many IR responses as the user wants to create
# their own custom IR and in turn filter. this script will perform convolution
# on each IR and return it is a numpy vector in the end
# inputs will be the IR wav files, as many as you want can be added

import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os


# class used to generate a new IR based on the input IR's
class IR_Generator:
    def __init__(self, *args): #input all IR's
        self.inputs = args
        
    # use method New_IR to generate them
    def New_IR(self):
        initial_data,initial_rate = sf.read(self.inputs[0]) #extract first entry
        if len(initial_data.shape) > 1 and initial_data.shape[1] == 2:  # Check if impulse is stereo
                    initial_data = np.mean(initial_data, axis=1)
        normalized_initial_impulse = initial_data / np.max(np.abs(initial_data))
        # section automatically removes silence from IR data to increase efficiency
        noise_threshold = 10**(-3) #change this to edit IR and how much is cut
        above_threshold_indices = np.where(abs(normalized_initial_impulse) > noise_threshold)[0]
        if len(above_threshold_indices) > 0: #grabs the important parts of the IR file
            IR_start_index = above_threshold_indices[0]
            IR_end_index = above_threshold_indices[-1]
        else:
            IR_start_index = 0
            IR_end_index = 0
        #Extract and concatenate the non_silent sections
        adjusted_normalized_initial_impulse = normalized_initial_impulse[IR_start_index:IR_end_index+1]
        try:
            for IR in self.inputs[1:]: #loop through second entry to last
                ir_data, ir_rate = sf.read(IR)
                if len(ir_data.shape) > 1 and ir_data.shape[1] == 2:  # Check if impulse is stereo
                    ir_data = np.mean(ir_data, axis=1)
                normalized_impulse = ir_data / np.max(np.abs(ir_data))
                
                above_threshold_indices = np.where(abs(normalized_impulse) > noise_threshold)[0]
                if len(above_threshold_indices) > 0: #grabs the important parts of the IR file
                    IR_start_index = above_threshold_indices[0]
                    IR_end_index = above_threshold_indices[-1]
                else:
                    IR_start_index = 0
                    IR_end_index = 0
                #Extract and concatenate the non_silent sections
                adjusted_normalized_impulse = normalized_impulse[IR_start_index:IR_end_index+1]
                
                # Resample IR based on our input IR sample rate
                if initial_rate != ir_rate:
                    num_samples = int(len(adjusted_normalized_impulse) * initial_rate / ir_rate)
                    ir_resampled = resample(adjusted_normalized_impulse, num_samples)
                else:
                    ir_resampled = adjusted_normalized_impulse
                    
                #check which signal needs to be padded
                if len(ir_resampled)<len(initial_data):
                    desired_length = len(adjusted_normalized_initial_impulse)
                    padded_impulse = np.pad(ir_resampled,(0, desired_length - len(ir_resampled)))
                    ir_resampled=padded_impulse
                if len(ir_resampled)>len(initial_data): #pad initial if its shorter signal
                    desired_length = len(ir_resampled)
                    padded_impulse = np.pad(adjusted_normalized_initial_impulse,(0, desired_length - len(adjusted_normalized_initial_impulse)))
                    adjusted_normalized_initial_impulse=padded_impulse
                     
                #put IR's together by convolution
                ir_resampled_fft = np.fft.fft(ir_resampled)
                initial_data_fft = np.fft.fft(adjusted_normalized_initial_impulse)
                combined_impulse_fft = ir_resampled_fft*initial_data_fft
                combined_impulse = np.real(np.fft.ifft(combined_impulse_fft))
                initial_data = combined_impulse #update IR to be combination of IR's
            if len(initial_data.shape) > 1 and initial_data.shape[1] == 2:  # Check if impulse is stereo
                initial_data = np.mean(initial_data, axis=1)  
        except: # if there is only 1 IR
            return adjusted_normalized_initial_impulse, initial_rate
        finally:
            return initial_data, initial_rate
        


#Example of How to use it
# First load wanted IR Files
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# tube_radio_IR= os.path.join(parent_dir, 'IR_Files', 'Erres_tube_radio.wav')
# Fender_Twin_Reverb_IR= os.path.join(parent_dir, 'IR_Files', 'Fender_Twin_Reverb.wav')
# Test1_IR = os.path.join(parent_dir, 'IR_Files', 'test1.wav')

# # Now initialize class by passing all wav files
# # next use the New_IR() method inside to generate our new Impulse response
# my_instance = IR_Generator(tube_radio_IR, Fender_Twin_Reverb_IR, Test1_IR) 

# IR_DATA,IR_RATE = my_instance.New_IR()