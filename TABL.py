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
# In that case, you may also want to change the content of "instruments" variable
fluidsynth.init("TimGM6mb.sf2", "pulseaudio")
fluidsynth.set_instrument(1, 5, 0)
instruments = range(0,127)

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
last_prog = None
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

def pick_instrument(instru=-1):
    fluidsynth.stop_everything()
    if instru != 0:
        fluidsynth.set_instrument(1, random.choice(instruments), 0)
    else:
        fluidsynth.set_instrument(1, instru, 0)
    

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

def get_chords(note_list, sevenths=False):
    valid_chords = list()
    i = 0
    for degree in note_list:
        if sevenths is True:
            chords = [ note_list[i], note_list[(i+2)%(len(note_list)-1)], note_list[(i+4)%(len(note_list)-1)], note_list[(i+6)%(len(note_list)-1)] ]
        else:
            chords = [ note_list[i], note_list[(i+2)%(len(note_list)-1)], note_list[(i+4)%(len(note_list)-1)] ]
        valid_chords.append(chords)
        i += 1
    return valid_chords
    
def play_scale(tonic, scale):
    valid_notes = get_scale(tonic, scale)
    
    update_gui(valid_notes)
    print("Valid notes: "+" ".join(valid_notes))
    
    octave = 3 if valid_notes[0][0] == 'C' else 4
    
    gui.after(1, lambda: switch_buttons(disable=True))
    gui.after(1, lambda: play_note(octave, valid_notes))
    gui.after((len(valid_notes)-1)*int(time_step*1000), lambda: switch_buttons(disable=False))
    
def play_note(octave, scale, count=0):
    if count == len(scale):
        return
    
    if scale[count][0] == 'C':
        octave += 1
    play_gui.config(text=scale[count]+"-"+str(octave))
    fluidsynth.play_Note(Note(scale[count]+"-"+str(octave)))
    gui.after(int(time_step*1000), lambda: play_note(octave, scale, count+1))
    
def play_random_prog(tonic=False, scale=False, sevenths=False, length=4):
    if tonic is False or scale is False:
        tonic = current_tonic
        scale = current_scale
    
    valid_notes = get_scale(tonic, scale)
    valid_chords = get_chords(valid_notes, sevenths)
    update_gui(valid_notes)
    
    random_chords = list()
    
    for i in range(0,length):
        random_chords.append(valid_chords[random.randint(0,len(valid_chords)-1)])
    
    if sevenths is True:
        print("Random sevenths in {}: ".format(current_tonic+" "+current_scale))
    else:
        print("Random triads in {}: ".format(current_tonic+" "+current_scale))
    for chords in random_chords:
        print("\t"+" ".join(chords))
    
    global last_prog; last_prog = random_chords
    play_gui.config(text="")
    gui.after(1, lambda: switch_buttons(disable=True))
    gui.after(1, lambda: play_chords(random_chords,random_mode=True))
    gui.after((len(random_chords)-1)*1000, lambda: switch_buttons(disable=False))
    
def play_all_chords(tonic=False, scale=False, sevenths=False):
    if tonic is False or scale is False:
        tonic = current_tonic
        scale = current_scale
    
    valid_notes = get_scale(tonic, scale)
    valid_chords = get_chords(valid_notes, sevenths)
    update_gui(valid_notes)
               
    if sevenths is True:
        print("Sevenths in {}: ".format(current_tonic+" "+current_scale))
    else:
        print("Triads in {}: ".format(current_tonic+" "+current_scale))
    for chords in valid_chords:
        print("\t"+" ".join(chords))
    
    gui.after(1, lambda: switch_buttons(disable=True))
    gui.after(1, lambda: play_chords(valid_chords))
    gui.after((len(valid_chords)-1)*int(time_step*1000), lambda: switch_buttons(disable=False))
        
def play_chords(chords_list, count=0, random_mode=False):
    if count == len(chords_list):
        return
    
    if random_mode is True:
        play_gui.config(text=play_gui["text"]+"\n"+" ".join(chords_list[count]))
        fluidsynth.play_NoteContainer(NoteContainer(chords_list[count]))
        gui.after(1000, lambda: play_chords(chords_list,count+1, random_mode))
    else:
        play_gui.config(text=chords_list[count])
        fluidsynth.play_NoteContainer(NoteContainer(chords_list[count]))
        gui.after(int(time_step*1000), lambda: play_chords(chords_list,count+1, random_mode))
    
def update_gui(valid_notes):
    scale = current_scale
    hexa_code = hex(int(scales[scale][1], 16) + int(notes_dict[valid_notes[0]]))[2:]

    gui.configure(bg="#"+hexa_code)
    note_gui.config(bg="#"+hexa_code, text=valid_notes[0]+"\n"+scale)
    scale_gui.config(text=" ".join(valid_notes), bg="#"+hexa_code)
    
    widgets = gui.winfo_children()
    for widget in widgets:
        if isinstance(widget, Scale):
            widget.config(bg="#"+hexa_code, fg="#FFFFFF", troughcolor="#000000")
        if isinstance(widget, Label) and widget["text"] == "Instrument":
            widget.config(bg="#"+hexa_code, fg="#FFFFFF")
    play_gui.config(bg="#"+hexa_code)
    
def randomize_selection():
    global current_tonic
    global current_scale
    current_tonic = random.choice(notes)
    current_scale = random.choice(list(scales.keys()))
    pick_instrument(-1)
    play_selection(current_tonic, current_scale)
    
def note_selection(tonic):
    global current_tonic
    current_tonic = tonic
    widgets = gui.winfo_children()
    for widget in widgets:
        if isinstance(widget, Button) and widget["text"] in notes_f:
            if widget["text"] == tonic:
                widget.config(bg="#FF0000", fg="#000000")
            else:
                if len(widget["text"]) == 1:
                    widget.config(bg="#FFFFFF", fg="#000000")
                else:
                    widget.config(bg="#000000", fg="#FFFFFF")
    play_selection(current_tonic, current_scale)
    
def scale_selection(scale):
    global current_scale
    current_scale = scale
    widgets = gui.winfo_children()
    for widget in widgets:
        if isinstance(widget, Button) and widget["text"] in list(scales.keys()):
            if widget["text"] == scale:
                widget.config(bg="#FF0000", fg="#000000")
            else:
                widget.config(bg="#FF8000", fg="#000000")

def replay_last():
    if last_prog is not None:
        play_gui.config(text="")
        gui.after(1, lambda: switch_buttons(disable=True))
        gui.after(1, lambda: play_chords(last_prog,random_mode=True))
        gui.after((len(last_prog)-1)*1000, lambda: switch_buttons(disable=False))
    else:
        play_selection()
    
def play_selection(tonic=False, scale=False):
    if tonic is False or scale is False:
        tonic = current_tonic
        scale = current_scale
    play_scale(tonic, scale)
    
    
random_b = Button(gui, text = "Randomize", command=randomize_selection).place(relx=0.05, rely=0.95, anchor=SW)
replay_b = Button(gui, text = "Replay", command=replay_last).place(relx=0.75, rely=0.95, anchor=SW)

instru_t = Label(gui, text="Instrument", bg="black", fg="white", font=("Helvetica", 10)).place(relx=0.5, rely=0.91, anchor=S)
instru_s = Scale(gui, from_=0, to=127, showvalue=0, bg="#000000", relief=SUNKEN, resolution = 1, orient=HORIZONTAL, command=pick_instrument, length=200).place(relx=0.5, rely=0.95, anchor=S)

triads_b = Button(gui, text = "Triads", command=play_all_chords).place(relx=0, rely=0.5, anchor=W)
sevens_b = Button(gui, text = "Sevenths", command= lambda: play_all_chords(sevenths=True)).place(relx=0, rely=0.6, anchor=W)
rdprog_b = Button(gui, text = "Random prog", command= lambda: play_random_prog(sevenths=False)).place(relx=0, rely=0.7, anchor=W)

notes_b = list()
drift = 0.02
for note in notes:
    callback = Callback(note_selection, note)
    if note == current_tonic:
        notes_b.append(Button(gui, bg='#FF0000', fg ='#000000', height=2, width=1, text = note, command=callback).place(relx=drift, rely=0, anchor=NW))
        drift += 0.08
        continue
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
note_gui.place(relx=0.5, rely=0.3, anchor=CENTER)
scale_gui.place(relx=0.5, rely=0.8, anchor=CENTER)
play_gui.place(relx=0.5, rely=0.7, anchor=S)

scale_selection(current_scale)

gui.mainloop()
