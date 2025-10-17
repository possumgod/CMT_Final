import math

# list of the notes: functions treat this as a cyclic list (loops from 'A' to 'G#')
notes_array = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]
equal_notes = {"Ab":"G#", "A#": "Bb", "Cb": "B", "Db": "C#", "D#": "Eb", "Fb":"E", "Gb": "F#"}

# returns equivalent note if not given from the default array
def note_equivalence(note):
    if note in equal_notes.keys():
        return equal_notes[note]
    return note

# returns the minimum distance between 2 given notes
def find_note_dist(n1, n2):
    n1i = notes_array.index(note_equivalence(n1))
    n2i = notes_array.index(note_equivalence(n2))
    return min((n1i - n2i) % 12, (n2i - n1i) % 12)

# splits notes from string to list of list of notes ('A B | F' -> [['A'. 'B'], ['F']])
def split_notes(note_str):
    n_seq = note_str.strip().split("|")
    return [i.strip().split(" ") for i in n_seq]

# euclidian distance between two numbers
def euclidian_dist(c_dist, n_dist):
    return math.sqrt(c_dist*c_dist + n_dist*n_dist)

# takes a dictionary from calc_chord_similarity and calcs the sqrt of the sum of squares of the vals
def euclidian_mult_weights(chord_dict):
    temp = 0
    for c in chord_dict.keys():
        temp += chord_dict[c] * chord_dict[c]
    return math.sqrt(temp)
