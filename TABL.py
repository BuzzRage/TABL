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

note_gui  = Label(gui, text="", bg="black", pady=50, font=("Helvetica", 40))
scale_gui = Label(gui, text="", bg="black", fg="black", font=("Helvetica", 20))
gui.configure(bg="black")

def play_scale(scale, tonic, mute=False):
    if scale is "major":
        valid_notes = s.Major(tonic).ascending()
    elif scale is "natural minor":
        valid_notes = s.NaturalMinor(tonic).ascending()
    elif scale is "harmonic minor":
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
        
def randomize_selection(mute=False):
    note  = random.choice(notes)
    scale = random.choice(list(scales.keys()))
    gui.configure(bg="#"+scales[scale][1])
    note_gui.config(bg="#"+scales[scale][1], text=note+"\n"+scale)
    valid_notes = play_scale(scale, note, mute)
    scale_gui.config(text=valid_notes, bg="#"+scales[scale][1])
    return (note, scale)


random_b = Button(gui, text = "Randomize", command=randomize_selection).pack()
note_gui.pack()
scale_gui.pack()

gui.mainloop()
