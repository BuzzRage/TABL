#!/usr/bin/env python3

import random
from tkinter import *

gui =Tk()
gui.geometry("400x200")
gui.title("Tool-Assisted Backing Loop")

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

note_gui = Label(gui, text="", bg="black", pady=100, font=("Helvetica", 40))
gui.configure(bg="black")

def randomize_selection():
    note  = random.choice(notes)
    scale = random.choice(list(scales.keys()))
    gui.configure(bg="#"+scales[scale][1])
    note_gui.config(bg="#"+scales[scale][1], text=note+"\n"+scale)
    return (note, scale)

selected_note,selected_scale = randomize_selection() 


random_b = Button(gui, text = "Randomize", command=randomize_selection).pack()
note_gui.pack()
note_gui.configure(text=selected_note+"\n"+selected_scale, bg="#"+scales[selected_scale][1])
gui.configure(bg="#"+scales[selected_scale][1])
gui.mainloop()

print("Tonic key: {}".format(selected_note))
print("Scale: {}".format(selected_scale))
