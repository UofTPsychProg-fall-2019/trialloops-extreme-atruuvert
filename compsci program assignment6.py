#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 2
Use this template to turn Step 1 into a loop
@author: katherineduncan
"""
#%% Required set up 

import numpy as np
import pandas as pd
import os, sys, csv
from psychopy import visual, core, event, gui, logging
import random
from random import shuffle
from psychopy.hardware import keyboard

defaultKeyboard = keyboard.Keyboard()
event.globalKeys.add(key='q', func=core.quit)

expInfo = {"SubjectNumber":'',"Age":'',"Gender":'',"Handedness":''}
subgui = gui.DlgFromDict(expInfo)

if subgui.OK == False:
    core.quit()  # user pressed cancel

# Save the data
subNum = expInfo["SubjectNumber"]
age = expInfo["Age"]
gend = expInfo["Gender"]
hand = expInfo["Handedness"]

# Open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='grey', unit='height') 

# Set up timer
trialClock = core.Clock()

# Setting up instructions
welcome_text = visual.TextStim(win=win, name='welcome_text',
    text='Welcome to the experiment.\n\nIn this experiment, you will be using the j and k keys to detect a target as quickly and accurately as possible.\n\nPress space to continue.',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

Instructions = visual.TextStim(win=win, name='Instructions',
    text='On every trial, a central fixation cross will appear.Keeping your eyes on the central fixation cross, press space, and the trial will begin. Then, the target will appear.\n\nPress space to continue.',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

instructions_part2 = visual.TextStim(win=win, name='instructions_part2',
    text='Your task is to indicate with the "j" and "k" keys what side the target appeared on ("j" being left and "k" being right), keeping your eyes at central fixation.\n\nPress space to begin.',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Setting up feedback

correct = visual.TextStim(win=win,
    text='Great!',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

incorrect = visual.TextStim(win=win,
    text='Error. j is left, k is right.',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Setting up start of trial (fixation cross)

fixation_start = visual.TextStim(win=win, name='fixation_start',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Setting up target

# Right
target_R =  visual.Circle(win=win,
    radius=0.015, 
    lineWidth=5, lineColor='black',
    lineColorSpace='rgb', fillColor='black',
    pos=(0.5,0), ori=0.0, opacity=1); 

# Left
target_L = visual.Circle(win=win,
    radius=0.015, 
    lineWidth=5, lineColor='black',
    lineColorSpace='rgb', fillColor='black',
    pos=(-0.5,0), ori=0.0, opacity=1); 
    
# **************************************************************************************************************
with open('{}.csv'.format(subNum), 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['subNum', 'age', 'gend', 'hand','trial', 'cond', 'target_side', 'key and RT', 'accuracy'])
    
    conditions = [0, 0.100, 0.150, 0.200, 0.250, 0.300]*2
    sides = ['L','R']*6
    
    def trial():
        
        event.clearEvents()
        
        cond = conditions[t]
        target_side = sides[t]
        
        accuracy = 'incorrect' # becomes correct if they press the correct key
        
        if target_side == 'L':
            target = target_L
        elif target_side == 'R':
            target = target_R
            
        fixation_start.draw()
        win.flip()
        keys=event.waitKeys(keyList='space')
        
        core.wait(cond)
        
        trialClock.reset()
        fixation_start.draw()
        target.draw()
        win.flip()
        
        keys=event.waitKeys(keyList=['j','k'], timeStamped=trialClock)
        
        if target_side == 'L' and keys[0][0] == 'j':
            accuracy = 'correct'
            correct.draw()
            win.flip()
            core.wait(3)
        elif target_side == 'R' and keys[0][0] == 'k':
            accuracy = 'correct'
            correct.draw()
            win.flip()
            core.wait(3)
        else:
            incorrect.draw()
            win.flip()
            core.wait(3)
        
        print('The key and reaction time was {}. The keypress was {}.'.format(keys, accuracy))
        writer.writerow([subNum, age, gend, hand, t, cond, target_side, keys, accuracy])
        
    
    # Loop through instructions 
    
    welcome_sequence = [welcome_text, Instructions, instructions_part2]
    for item in welcome_sequence:
        event.clearEvents()
        item.draw()
        win.flip()
        keys = event.waitKeys(keyList='space')
    
    # Loop through experiment trials
    
    shuffle(conditions)
    shuffle(sides)
    
    t = 0
    while t in range(12):
        trial()
        t+=1
        

#%% Required clean up

core.wait(2)
win.close()