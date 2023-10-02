#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 13:20:21 2023

@author: pi
"""

#This code makes the GUI for our pedal that shows the names of our IR and 
# allows you to click them 


import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
import os
import sys
from IR_Generator import IR_Generator

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                             QLabel, QCheckBox, QHBoxLayout, QScrollArea, QFrame)
from PyQt5.QtCore import Qt

class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.folder_path = os.path.join(parent_dir, 'IR_Files')
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        
        self.containerWidget = QWidget()
        self.layout = QVBoxLayout(self.containerWidget)
        self.scrollArea.setWidget(self.containerWidget)

        self.addFileButtons(self.folder_path)

        mainLayout.addWidget(self.scrollArea)
        self.setLayout(mainLayout)

        self.setGeometry(200, 200, 300, 400)
        self.setWindowTitle('File Browser')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)  # Add maximize button

        self.generateIRButton = QPushButton('Generate IR', self)
        self.generateIRButton.clicked.connect(self.generateIRClicked)
        mainLayout.addWidget(self.generateIRButton)

        self.show()
        #%% Creates the buttons
    def addFileButtons(self, folder_path):
        from os import listdir
        from os.path import isfile, join

        # Dictionary to record file selection
        self.fileSelection = {}

        # List all files in the directory
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

        for file_name in files:
            hLayout = QHBoxLayout()  # Use a horizontal layout to place checkbox and button

            checkbox = QCheckBox(self)
            hLayout.addWidget(checkbox)
            checkbox.stateChanged.connect(lambda state, file=file_name: self.updateFileSelection(file, state))

            btn = QPushButton(file_name, self)
            btn.clicked.connect(lambda checked, chkbox=checkbox: chkbox.setChecked(not chkbox.isChecked()))
            hLayout.addWidget(btn)

            # Add the horizontal layout to the main vertical layout
            self.layout.addLayout(hLayout)

            # Initialize file selection dictionary
            self.fileSelection[file_name] = False
    #%% grabs out selected IRs
    def updateFileSelection(self, file_name, state):
        self.fileSelection[file_name] = state == Qt.Checked
        selected_files = [key for key, value in self.fileSelection.items() if value]
        print("Selected files:", selected_files)
    #%% Used to generate new IR and send it to live audio
    def generateIRClicked(self):
        print("Generate IR button clicked!")
        # Add your IR generation logic here
        # For instance, you can use the selected files to generate an IR
        # and if you have a function called 'generateIR' in IR_Generator, you could call:
        # IR_Generator.generateIR(selected_files)
        selected_files = [key for key, value in self.fileSelection.items() if value]
        stored_files = []
        if selected_files:
            # parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            # tube_radio_IR= os.path.join(parent_dir, 'IR_Files', 'Erres_tube_radio.wav')
            # Test1_IR = os.path.join(parent_dir, 'IR_Files', 'test1.wav')
            # use this to call generator create function and make our custom IR
            for files in selected_files:
                parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                stored_files.append(os.path.join(parent_dir, 'IR_Files', files))
            my_instance = IR_Generator(*stored_files) # loads in all IR files to make our new one
            IR_DATA,IR_RATE=my_instance.New_IR()
            self.PlayAudio(IR_DATA,IR_RATE) # now send IR to our audio so we can use it for live audio
        else:
            print("No files selected for IR generation!")
    #%% For live audio with our new IR      
    def PlayAudio(self,irdata,irrate):
        print('stuff')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileBrowser()
    sys.exit(app.exec_())

