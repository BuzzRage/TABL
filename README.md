# TABL
Tool-Assisted Backing Loop

A simple music tool that generates chords progression based on a tonic key and a scale (that both may be either chosen or picked randomly).

This works with `Tkinter` for the GUI, and `fluidsynth` for the sound. You may need to change the audio driver for your operating system. `PulseAudio` should work on modern Linux distributions. 

You can change the soundfont to another (by default, this program uses `TimGM6mb.sf2` which is light enough to be provided within a github repository).


## TO DO

* Let the user choose a scale
* Improve scale display by putting a tabulation for each semitone not valid in a scale
* Generate a random chord progression that loops
* Add a button to see all triads
* Add a button to listan and see all sevenths
* Build a transcoder from binary representation of tones into actual scale (i.e. 101011010101 = Major)
* When playing a chords, change color of played notes in the scale label
* Let the user choose the time step

## Done

* Randomly generate a tonic and a scale, play the scale and print the valid notes
* Add a button to randomize again
* Add a replay button
* Make the tonic change the color (e.g. A = 440 Hz, add 0x440 to the hexacode of a scale)
* Let the user choose a tonic note
* Add a button to listen all triads of the current scale and last selected tonic
