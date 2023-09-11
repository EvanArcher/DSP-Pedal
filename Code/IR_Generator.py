#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 17:27:10 2023

@author: pi
"""

#This class is designed to take as many IR responses as the user wants to create
# their own custom IR and in turn filter. this script will perform convolution
# on each IR and return it is a numpy vector in the end
# inputs will be the IR wav files

import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os

class IR_Generator:
    def __init__(self, *args):
        self.inputs = args
        
    def New_IR(self):
        initial_data,initial_rate = sf.read(self.inputs[0]) #extract first entry
        try:
            for IR in self.inputs[1:]: #loop through second entry to last
                ir_data, ir_rate = sf.read(IR)
                # Resample IR based on our other IR sample rate
                if initial_rate != ir_rate:
                    num_samples = int(len(ir_data) * initial_rate / ir_rate)
                    ir_resampled = resample(ir_data, num_samples)
                else:
                    ir_resampled = ir_data
                
                print("Inputs:", ir_rate, IR)
        except: # if there is only 1 IR
            return initial_data, initial_rate
        finally:
            return initial_data, initial_rate
        

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

tube_radio_IR= os.path.join(parent_dir, 'IR_Files', 'Erres_tube_radio.wav')
Fender_Twin_Reverb_IR= os.path.join(parent_dir, 'IR_Files', 'Fender_Twin_Reverb.wav')
Test1_IR = os.path.join(parent_dir, 'IR_Files', 'test1.wav')



my_instance = IR_Generator(tube_radio_IR, Fender_Twin_Reverb_IR, Test1_IR)

IR_DATA,IR_RATE = my_instance.New_IR()