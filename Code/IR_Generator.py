#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 17:27:10 2023

@author: pi
"""

#This script is designed to take as many IR responses as the user wants to create
# their own custom IR and in turn filter. this script will perform convolution
# on each IR and return it is a numpy vector in the end

import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os

class IR_Generator:
    def __init__(self, *args):
        self.inputs = args
        
    def print_inputs(self):
        print("Inputs:", self.inputs)
        

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

tube_radio_IR= os.path.join(parent_dir, 'IR_Files', 'Erres_tube_radio.wav')
Fender_Twin_Reverb_IR= os.path.join(parent_dir, 'IR_Files', 'Fender_Twin_Reverb.wav')



my_instance = IR_Generator(tube_radio_IR, Fender_Twin_Reverb_IR)

my_instance.print_inputs()