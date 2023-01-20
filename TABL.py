#!/usr/bin/env python3

import random
from time import sleep
from tkinter import *
import mingus.core.keys as k
import mingus.core.scales as s
from mingus.containers import *
from mingus.midi import fluidsynth

gui =Tk()
gui.geometry("400x300")
gui.title("Tool-Assisted Backing Loop")

# You may want to change the soundfont file or the audio driver !
fluidsynth.init("TimGM6mb.sf2", "pulseaudio")

notes = ["C","C#","D","Eb","E","F","F#","G","Ab","A","Bb","B"]
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

note_gui  = Label(gui, text="", bg="black", pady=50, font=("Helvetica", 40))
scale_gui = Label(gui, text="", bg="black", fg="black", font=("Helvetica", 20))
gui.configure(bg="black")

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
    scale = " ".join(s.determine(valid_notes)[0].split(" ")[1:])
    gui.configure(bg="#"+scales[scale][1])
    note_gui.config(bg="#"+scales[scale][1], text=valid_notes[0]+"\n"+scale)
    scale_gui.config(text=valid_notes, bg="#"+scales[scale][1])
    
def randomize_selection():
    global current_tonic
    global current_scale
    current_tonic = random.choice(notes)
    current_scale = random.choice(list(scales.keys()))
    play_selection(current_tonic, current_scale)

def play_selection(tonic=False, scale=False, mute=False):
    if tonic is False or scale is False:
        tonic = current_tonic
        scale = current_scale
    valid_notes = play_scale(scale, tonic, mute)
    update_gui(valid_notes)
    


random_b = Button(gui, text = "Randomize", command=randomize_selection).place(relx=0.3, rely=0.9, anchor=CENTER)
replay_b = Button(gui, text = "Replay", command=play_selection).place(relx=0.6, rely=0.9, anchor=CENTER)
note_gui.pack()
scale_gui.pack()

gui.mainloop()
