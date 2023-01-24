#!/usr/bin/env python3

import random
from time import sleep
from tkinter import *
import mingus.core.keys as k
import mingus.core.scales as s
from mingus.containers import *
from mingus.midi import fluidsynth

gui =Tk()
gui.geometry("500x500")
gui.title("Tool-Assisted Backing Loop")

# You may want to change the soundfont file or the audio driver !
fluidsynth.init("TimGM6mb.sf2", "pulseaudio")

notes = ["C","C#","D","Eb","E","F","F#","G","Ab","A","Bb","B"]
notes_f = ["C","C#","Db","D","D#","Eb","E","Fb","E#","F","F#","Gb","G","G#","Ab","A","A#","Bb","B","Cb","B#"]
notes_hz = [261.625, 277.182, 277.182, 293.664, 311.126, 311.126, 329.627, 329.627, 349.228, 349.228, 369.994, 369.994, 391.995, 415.304, 415.304, 440.000, 466.163, 466.163, 493.883, 493.883, 261.625]
notes_dict = dict(zip(notes_f, notes_hz))
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

time_step = 0.4

note_gui  = Label(gui, text="", bg="black", pady=30, font=("Helvetica", 40))
scale_gui = Label(gui, text="", bg="black", fg="black", font=("Helvetica", 20))
play_gui  = Label(gui, text="", bg="black", fg="#FF0000", font=("Helvetica", 20))
gui.configure(bg="black")

class Callback:
    def __init__(self, callback, *firstArgs):
        self.__callback = callback
        self.__firstArgs = firstArgs

    def __call__(self, *args):
        return self.__callback (*(self.__firstArgs + args))

def switch_buttons(disable=False):
    widgets = gui.winfo_children()
    for widget in widgets:
        if isinstance(widget, Button):
            if disable is True:
                widget.config(state="disabled")
            else:
                widget.config(state="normal")

def get_scale(tonic, scale):
    if scale == "major":
        valid_notes = s.Major(tonic).ascending()
    elif scale == "natural minor":
        valid_notes = s.NaturalMinor(tonic).ascending()
    elif scale == "harmonic minor":
        valid_notes = s.HarmonicMinor(tonic).ascending()
    else:
        print("Error: Invalid scale provided in get_scale()")
    return valid_notes
    
def play_scale(tonic, scale):
    valid_notes = get_scale(tonic, scale)
    
    update_gui(valid_notes)
    print("Valid notes: "+" ".join(valid_notes))
    
    octave = 3 if valid_notes[0][0] == 'C' else 4
    
    gui.after(1, lambda: switch_buttons(disable=True))
    gui.after(1, lambda: play_note(octave, valid_notes))
    gui.after((len(valid_notes)-1)*int(time_step*1000), lambda: switch_buttons(disable=False))
    
def play_note(octave, scale,count=0):
    if count == 8:
        return
    
    if scale[count][0] == 'C':
        octave += 1
    play_gui.config(text=scale[count]+"-"+str(octave))
    fluidsynth.play_Note(Note(scale[count]+"-"+str(octave)))
    gui.after(int(time_step*1000), lambda: play_note(octave, scale, count+1))
    
def play_triads(tonic=False, scale=False):
    if tonic is False or scale is False:
        tonic = current_tonic
        scale = current_scale
    
    valid_chords = list()
    valid_notes = get_scale(tonic, scale)
    i = 0
    
    print("Valid chords: ")
    
    for degree in valid_notes:
        chords = [ valid_notes[i], valid_notes[(i+2)%(len(valid_notes)-1)], valid_notes[(i+4)%(len(valid_notes)-1)] ]
        valid_chords.append(chords)
        print("\t"+" ".join(chords))
        i += 1
    
    gui.after(1, lambda: switch_buttons(disable=True))
    gui.after(1, lambda: play_chords(valid_chords))
    gui.after((len(valid_notes)-1)*int(time_step*1000), lambda: switch_buttons(disable=False))
        
def play_chords(chords_list, count=0):
    if count == 8:
        return
    
    play_gui.config(text=chords_list[count])
    fluidsynth.play_NoteContainer(NoteContainer(chords_list[count]))
    gui.after(int(time_step*1000), lambda: play_chords(chords_list,count+1))
    
def update_gui(valid_notes):
    scale = current_scale
    hexa_code = hex(int(scales[scale][1], 16) + int(notes_dict[valid_notes[0]]))[2:]

    gui.configure(bg="#"+hexa_code)
    note_gui.config(bg="#"+hexa_code, text=valid_notes[0]+"\n"+scale)
    scale_gui.config(text=" ".join(valid_notes), bg="#"+hexa_code)
    play_gui.config(bg="#"+hexa_code)
    
def randomize_selection():
    global current_tonic
    global current_scale
    current_tonic = random.choice(notes)
    current_scale = random.choice(list(scales.keys()))
    play_selection(current_tonic, current_scale)
    
def note_selection(tonic):
    global current_tonic
    current_tonic = tonic
    play_selection(current_tonic, current_scale)
    
def scale_selection(scale):
    global current_scale
    current_scale = scale
    play_selection(current_tonic, current_scale)
    
def play_selection(tonic=False, scale=False):
    if tonic is False or scale is False:
        tonic = current_tonic
        scale = current_scale
    play_scale(tonic, scale)
    
    
random_b = Button(gui, text = "Randomize", command=randomize_selection).place(relx=0.2, rely=0.9, anchor=CENTER)
replay_b = Button(gui, text = "Replay", command=play_selection).place(relx=0.6, rely=0.9, anchor=CENTER)
triads_b = Button(gui, text = "Triads", command=play_triads).place(relx=0.8, rely=0.9, anchor=CENTER)

notes_b = list()
drift = 0.02
for note in notes:
    callback = Callback(note_selection, note)
    if len(note) == 1:
        notes_b.append(Button(gui, bg='#FFFFFF', fg ='#000000', height=2, width=1, text = note, command=callback).place(relx=drift, rely=0, anchor=NW))
    else:
        notes_b.append(Button(gui, bg='#000000', fg ='#FFFFFF', width=1, text = note, command=callback).place(relx=drift, rely=0, anchor=NW))
    drift += 0.08

scales_b = list()
drift = 0.5
for scale in list(scales.keys()):
    callback = Callback(scale_selection, scale)
    scales_b.append(Button(gui, text = scale, command=callback).place(relx=1, rely=drift, anchor=E))
    drift += 0.1
note_gui.place(relx=0.5, rely=0.4, anchor=CENTER)
scale_gui.place(relx=0.5, rely=0.8, anchor=CENTER)
play_gui.place(relx=0.5, rely=0.7, anchor=CENTER)

gui.mainloop()
