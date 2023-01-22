#!/usr/bin/env python3

import random
from time import sleep
from tkinter import *
import mingus.core.keys as k
import mingus.core.scales as s
from mingus.containers import *
from mingus.midi import fluidsynth

gui =Tk()
gui.geometry("400x400")
gui.title("Tool-Assisted Backing Loop")

# You may want to change the soundfont file or the audio driver !
fluidsynth.init("TimGM6mb.sf2", "pulseaudio")

notes = ["C","C#","D","Eb","E","F","F#","G","Ab","A","Bb","B"]
notes_hz = [261.625, 277.182, 293.664, 311.126, 329.627, 349.228, 369.994, 391.995, 415.304, 440.000, 466.163, 493.883]
notes_dict = dict(zip(notes, notes_hz))
major            = (1,0,1,0,1,1,0,1,0,1,0,1)
minor_natural    = (1,0,1,1,0,1,0,1,1,0,1,0)
minor_harmonique = (1,0,1,1,0,1,0,1,1,0,0,1)
major_hex            = format(0b101011010101, 'x')
minor_natural_hex    = format(0b101101011010, 'x')
minor_harmonique_hex = format(0b101101011001, 'x')
scales = {"major":            (major, major_hex), 
          "natural minor":    (minor_natural, minor_natural_hex), 
          "harmonic minor":   (minor_harmonique, minor_natural_hex)}
current_tonic = "C"
current_scale = "major"

note_gui  = Label(gui, text="", bg="black", pady=30, font=("Helvetica", 40))
scale_gui = Label(gui, text="", bg="black", fg="black", font=("Helvetica", 20))
gui.configure(bg="black")

class Callback:
    def __init__(self, callback, *firstArgs):
        self.__callback = callback
        self.__firstArgs = firstArgs

    def __call__(self, *args):
        return self.__callback (*(self.__firstArgs + args))

def play_scale(scale, tonic, mute=False):
    if scale == "major":
        valid_notes = s.Major(tonic).ascending()
    elif scale == "natural minor":
        valid_notes = s.NaturalMinor(tonic).ascending()
    elif scale == "harmonic minor":
        valid_notes = s.HarmonicMinor(tonic).ascending()
        
    if mute is True:
        return valid_notes
    
    octave = 3 if valid_notes[0][0] == 'C' else 4

    print(valid_notes)
    for n in valid_notes:
        if n[0] == 'C':
            octave += 1
        print(n+" " +str(octave))
        fluidsynth.play_Note(Note(n+"-"+str(octave)))
        sleep(0.5)
    
    return valid_notes
    
def update_gui(valid_notes):
    scale = current_scale
    hexa_code = hex(int(scales[scale][1], 16) + int(notes_dict[valid_notes[0]]))[2:]
    gui.configure(bg="#"+hexa_code)
    note_gui.config(bg="#"+hexa_code, text=valid_notes[0]+"\n"+scale)
    scale_gui.config(text=valid_notes, bg="#"+hexa_code)
    
def randomize_selection():
    global current_tonic
    global current_scale
    current_tonic = random.choice(notes)
    current_scale = random.choice(list(scales.keys()))
    play_selection(current_tonic, current_scale)
    
def user_selection(tonic):
    global current_tonic
    current_tonic = tonic
    play_selection(current_tonic, current_scale)
    
def play_selection(tonic=False, scale=False, mute=False):
    if tonic is False or scale is False:
        tonic = current_tonic
        scale = current_scale
    valid_notes = play_scale(scale, tonic, mute)
    update_gui(valid_notes)
    


random_b = Button(gui, text = "Randomize", command=randomize_selection).place(relx=0.3, rely=0.9, anchor=CENTER)
replay_b = Button(gui, text = "Replay", command=play_selection).place(relx=0.7, rely=0.9, anchor=CENTER)
notes_b = list()
drift = 0.11
for note in notes:
    callback = Callback(user_selection, note)
    if len(note) == 1:
        notes_b.append(Button(gui, bg='#FFFFFF', fg ='#000000', text = note, command=callback).place(relx=drift, rely=0.01, anchor=NE))
    else:
        notes_b.append(Button(gui, bg='#000000', fg ='#FFFFFF', text = note, command=callback).place(relx=drift, rely=0.12, anchor=NE))
    drift += 0.08
note_gui.place(relx=0.5, rely=0.4, anchor=CENTER)
scale_gui.place(relx=0.5, rely=0.8, anchor=CENTER)

gui.mainloop()
