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

gui.rowconfigure(0, weight=1)
gui.rowconfigure(1, weight=1)
gui.rowconfigure(2, weight=1)
gui.rowconfigure(3, weight=1)
gui.rowconfigure(4, weight=1)
gui.rowconfigure(5, weight=1)
gui.rowconfigure(6, weight=1)
gui.rowconfigure(7, weight=1)
gui.rowconfigure(8, weight=1)

gui.columnconfigure(0, weight=1)
gui.columnconfigure(1, weight=1)
gui.columnconfigure(2, weight=1)
gui.columnconfigure(3, weight=1)
gui.columnconfigure(4, weight=1)
gui.columnconfigure(5, weight=1)
gui.columnconfigure(6, weight=1)
gui.columnconfigure(7, weight=1)
gui.columnconfigure(8, weight=1)

# You may want to change the soundfont file or the audio driver !
# In that case, you may also want to change the content of "instruments" variable
fluidsynth.init("TimGM6mb.sf2", "pulseaudio")
instruments = range(0,127)
default_instrument = 5
fluidsynth.set_instrument(1, default_instrument, 0)


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
loop = False
loop_count = 0
default_time_step = 0.4
time_step = default_time_step


play_gui  = Label(gui, text="", bg="black", fg="#FF0000", font=("Helvetica", 20))
instru_t  = Label(gui, text="Instrument", bg="black", fg="white", font=("Helvetica", 10))
gui.configure(bg="black")

class Callback:
    def __init__(self, callback, *firstArgs):
        self.__callback = callback
        self.__firstArgs = firstArgs

    def __call__(self, *args):
        return self.__callback (*(self.__firstArgs + args))

def set_time_step(t_step=-1):
    global time_step;
    time_step = float(t_step)
    
def pick_instrument(instru=-1):
    fluidsynth.stop_everything()
    if instru != 0:
        fluidsynth.set_instrument(1, random.choice(instruments), 0)
    else:
        fluidsynth.set_instrument(1, instru, 0)
    

def switch_buttons(disable=False):
    widgets = gui.winfo_children()
    for widget in widgets:
        if isinstance(widget, Button) and widget["text"] not in ["Loop","Stop"]:
            if disable is True:
                widget.config(state="disabled")
            else:
                widget.config(state="normal")
                
def loop_button(disable=False):
    widgets = gui.winfo_children()
    for widget in widgets:
        if isinstance(widget, Button) and widget["text"] in ["Loop","Stop"]:
            if disable is True:
                widget.config(state="disabled")
            else:
                if last_prog is not None:
                    widget.config(state="normal")

def get_scale(tonic=None, scale=None):
    if tonic is None or scale is None:
        tonic = current_tonic
        scale = current_scale
    
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
    gui.after(1, lambda: loop_button(disable=True))
    gui.after(1, lambda: play_note(octave, valid_notes))
    gui.after((len(valid_notes)-1)*int(time_step*1000), lambda: switch_buttons(disable=False))
    gui.after((len(valid_notes)-1)*int(time_step*1000), lambda: loop_button(disable=False))
    gui.after((len(valid_notes)+2)*int(time_step*1000), fluidsynth.stop_everything)
    
def play_note(octave, scale, count=0):
    if count == len(scale):
        return
    
    if scale[count][0] == 'C':
        octave += 1
    play_gui.config(text=scale[count]+"-"+str(octave))
    fluidsynth.play_Note(Note(scale[count]+"-"+str(octave)))
    gui.after(int(time_step*1000), lambda: play_note(octave, scale, count+1))
    
def play_random_prog(tonic=None, scale=None, sevenths=False, length=4):
    if tonic is None or scale is None:
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
    
    global last_prog; last_prog = {"chords": random_chords, "tonic": tonic, "scale": scale}
    
    gui.after(1, lambda: switch_buttons(disable=True))
    gui.after(1, lambda: loop_button(disable=True))
    gui.after(1, lambda: play_chords(random_chords,random_mode=True))
    gui.after((len(random_chords)-1)*int(time_step*1000), lambda: switch_buttons(disable=False))
    gui.after((len(random_chords)-1)*int(time_step*1000), lambda: loop_button(disable=False))
    gui.after((len(random_chords)+2)*int(time_step*1000), fluidsynth.stop_everything)
    
def play_all_chords(tonic=None, scale=None, sevenths=False):
    if tonic is None or scale is None:
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
    gui.after(1, lambda: loop_button(disable=True))
    gui.after(1, lambda: play_chords(valid_chords))
    gui.after((len(valid_chords)-1)*int(time_step*1000), lambda: switch_buttons(disable=False))
    gui.after((len(valid_chords)-1)*int(time_step*1000), lambda: loop_button(disable=False))
    gui.after((len(valid_chords)+2)*int(time_step*1000), fluidsynth.stop_everything)
        
def play_chords(chords_list, count=0, random_mode=False):
    if count == len(chords_list):
        return
        
    play_gui.config(text= play_gui["text"]+"\n"+" ".join(chords_list[count]) if random_mode else chords_list[count])
    fluidsynth.play_NoteContainer(NoteContainer(chords_list[count]))
    gui.after(int(time_step*1000), lambda: play_chords(chords_list,count+1, random_mode))
    
def invert_color(hex_color):
    inverted = ""
    i = 0
    hexa_length = len(hex_color)
    
    if hexa_length == 3:
        hex_color = hex_color[0]+hex_color[0]+hex_color[1]+hex_color[1]+hex_color[2]+hex_color[2]
    else:
        for i in range(0,6):
            if i > hexa_length-1:
                hex_color = "0"+hex_color

    R = hex(255 - int(hex_color[0:2], 16))[2:]
    G = hex(255 - int(hex_color[2:4], 16))[2:]
    B = hex(255 - int(hex_color[4:6], 16))[2:]
    
    R = "0" + R if len(R) == 1 else R
    G = "0" + G if len(G) == 1 else G
    B = "0" + B if len(B) == 1 else B
    
    inverted = R+G+B

    return inverted
    
def update_gui(valid_notes):
    tonic = current_tonic
    scale = current_scale 
    play_text = ""
    hexa_code  = hex(int(scales[scale][1], 16) + int(notes_dict[valid_notes[0]]))[2:]
    invert_hex = invert_color(hexa_code)
    widgets = gui.winfo_children()
    for widget in widgets:
        if isinstance(widget, Scale):
            if widget["resolution"] == 1:
                widget.config(bg="#"+hexa_code, fg="#FFFFFF", troughcolor="#000000")
        if isinstance(widget, Label) and widget["text"] == "Instrument":
            widget.config(bg="#"+hexa_code, fg="#FFFFFF")
        if isinstance(widget, Button):
            if widget["text"] in notes_f:
                if widget["text"] == tonic:
                    widget.config(bg="#FF0000", fg="#000000")
                else:
                    if len(widget["text"]) == 1:
                        widget.config(bg="#FFFFFF", fg="#000000")
                    else:
                        widget.config(bg="#000000", fg="#FFFFFF")
                        
            elif widget["text"] in list(scales.keys()):
                if widget["text"] == scale:
                    widget.config(bg="#FF0000", fg="#000000")
                else:
                    widget.config(bg="#FF8000", fg="#000000")
                    
            elif widget["text"] in ["Loop", "Stop"]:
                if loop is True:
                    widget.config(bg="#00FF00", fg="#000000")
                    widget["text"] = "Stop"
                elif loop is False:
                    widget.config(bg="#FF0000", fg="#000000")
                    widget["text"] = "Loop"
            
    gui.configure(bg="#"+hexa_code)
    notes_frame.configure(bg="#"+hexa_code)
    time_frame.configure(bg="#"+hexa_code)
    note_gui.config(bg="#"+hexa_code, fg="#"+invert_hex,text=valid_notes[0]+"\n"+scale)
    scale_gui.config(text=" ".join(valid_notes), bg="#"+hexa_code)
    instru_t.config(fg="#"+invert_hex)
    play_gui.config(bg="#"+hexa_code, text=play_text)
    gui.after(1, fluidsynth.stop_everything)
    
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
    play_selection(current_tonic, current_scale)
    
def scale_selection(scale):
    global current_scale
    current_scale = scale
    update_gui(get_scale())

def replay_last(count=-1):        
    if loop is True:
        global loop_count; loop_count=count        
        if count%(len(last_prog["chords"])) == 0:
            gui.after(1, fluidsynth.stop_everything)
            play_gui.config(text="")
            gui.after(1, lambda: play_chords(last_prog["chords"],random_mode=True))
        gui.after(int(time_step*1000), lambda: replay_last(count+1))
    elif loop is False and count == -1:
        if last_prog is not None:
            global current_tonic; global current_scale;
            current_tonic = last_prog["tonic"]
            current_scale = last_prog["scale"]
            update_gui(get_scale(current_tonic, current_scale))
            gui.after(1, fluidsynth.stop_everything)
            gui.after(1, lambda: switch_buttons(disable=True))
            gui.after(1, lambda: loop_button(disable=True))
            gui.after(1, lambda: play_chords(last_prog["chords"],random_mode=True))
            gui.after((len(last_prog["chords"]))*int(time_step*1000), lambda: switch_buttons(disable=False))
            gui.after((len(last_prog["chords"]))*int(time_step*1000), lambda: loop_button(disable=False))
            gui.after((len(last_prog["chords"])+2)*int((time_step)*1000), fluidsynth.stop_everything)
        else:
            play_selection()
         
def stop_loop():
    loop_button(disable=False)
    switch_buttons(disable=False)
    play_text = play_gui["text"]
    global current_tonic; global current_scale;
    current_tonic = last_prog["tonic"]
    current_scale = last_prog["scale"]
    update_gui(get_scale(current_tonic, current_scale))
    play_gui.config(text=play_text)
     
def loop_last():
    global loop; global current_tonic; global current_scale;
    
    if last_prog["chords"] is None:
        return
    
    if not loop:
        loop = True
        global current_tonic; global current_scale;
        current_tonic = last_prog["tonic"]
        current_scale = last_prog["scale"]
        update_gui(get_scale(current_tonic, current_scale))
        gui.after(1, lambda: switch_buttons(disable=True))
        replay_last(count=0)
    else:
        loop = False
        gui.after(1, lambda: loop_button(disable=True))
        gui.after((len(last_prog["chords"])-(loop_count)%len(last_prog["chords"]))*int(time_step*1000), stop_loop)
        gui.after(((len(last_prog["chords"])+2)-(loop_count)%len(last_prog["chords"]))*int(time_step*1000), fluidsynth.stop_everything)
    
def play_selection(tonic=None, scale=None):
    if tonic is None or scale is None:
        tonic = current_tonic
        scale = current_scale
    play_scale(tonic, scale)
    
    

notes_frame = Frame(gui)
notes_frame.place(relx=0.5, rely=0, anchor=N)

notes_b = list()
curr_column = 1
for note in notes:
    callback = Callback(note_selection, note)
    if note == current_tonic:
        notes_b.append(Button(notes_frame, bg='#FF0000', fg ='#000000', height=2, width=1, text = note, command=callback).grid(column=curr_column, row=0, sticky=NW, padx=2))
        curr_column += 1
        continue
    if len(note) == 1:
        notes_b.append(Button(notes_frame, bg='#FFFFFF', fg ='#000000', height=2, width=1, text = note, command=callback).grid(column=curr_column, row=0, sticky=NW, padx=2))
    else:
        notes_b.append(Button(notes_frame, bg='#000000', fg ='#FFFFFF', width=1, text = note, command=callback).grid(column=curr_column, row=0, sticky=NW, padx=2))
    curr_column += 1

time_frame = Frame(gui)
time_frame.columnconfigure(0, weight=1)
time_frame.columnconfigure(1, weight=7)
#time_frame.columnconfigure(0, weight=1)
#time_frame.columnconfigure(0, weight=1)

tstep_s  = Scale(time_frame, from_=0.1, to=3, bg="#333333", fg="red", relief=SUNKEN, resolution = 0.1, command=set_time_step, length=100)
tstep_s.set(default_time_step)
tstep_s.grid(column=0, row=0, sticky=W)

note_gui = Label(time_frame, text="", bg="black", pady=30, padx=30, font=("Helvetica", 40), relief=SUNKEN)
note_gui.grid(column=1, row=0, sticky=EW)

#time_frame.place(relx=0, rely=0.3, anchor=W)
time_frame.grid(row=1, column=0, columnspan=8, sticky=EW)


layer2 = Frame(gui)
layer2.columnconfigure(0, weight=1)
layer2.columnconfigure(1, weight=6)
layer2.columnconfigure(2, weight=1)
triads_b  = Button(layer2, text = "Triads", command=play_all_chords).grid(row=0, column=0, sticky=W)
scale_gui = Label(layer2, text="", bg="black", fg="black", font=("Helvetica", 20))
scale_gui.grid(row=0, column=1)

sevens_b = Button(gui, text = "Sevenths", command= lambda: play_all_chords(sevenths=True)).grid(row=3, column=0, sticky=W)
rdprog_b = Button(gui, text = "Random prog", command= lambda: play_random_prog(sevenths=False)).grid(row=4, column=0, sticky=W)

scale_gui.grid(row=2, column=0, columnspan=8, sticky=W)
play_gui.place(relx=0.5, rely=0.7, anchor=S)

scales_b = list()
curr_row = 2
for scale in list(scales.keys()):
    callback = Callback(scale_selection, scale)
    if curr_row == 2:
        scales_b.append(Button(layer2, text = scale, command=callback).grid(row=curr_row, column=8, sticky=E))
    else:
        scales_b.append(Button(gui, text = scale, command=callback).grid(row=curr_row, column=8, sticky=E))
    curr_row += 1



random_b = Button(gui, text = "Randomize", command=randomize_selection).place(relx=0.05, rely=0.95, anchor=SW)
instru_t.place(relx=0.5, rely=0.91, anchor=S)
instru_s = Scale(gui, from_=0, to=127, showvalue=0, bg="#000000", relief=SUNKEN, resolution = 1, orient=HORIZONTAL, command=pick_instrument, length=200)
instru_s.set(default_instrument)
instru_s.place(relx=0.5, rely=0.95, anchor=S)
replay_b = Button(gui, text = "Replay", command=replay_last).place(relx=0.72, rely=0.95, anchor=SW)
loop_b   = Button(gui, text = "Loop", state="disabled", command=loop_last, bg="#FF0000", fg="#000000").place(relx=1, rely=0.95, anchor=SE)



scale_selection(current_scale)

gui.mainloop()
