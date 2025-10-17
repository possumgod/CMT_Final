# generates sample collection in collection directory

import random
import os
import V1.chord_similarity as cs
import V1.note_similarity as ns

# takes int from user to specify number of files, 20 by default (for now)
def gen_files(n=25, min=5, max=15):
    max = min + 5 if min >= max else max
    for i in range(n):
        with open(f"collection/piece{i + 1}.txt", "w") as curr_piece:
            chord_string = ""
            for i in range(random.randrange(min, max)):
                curr_ch = random.choice(list(cs.chord_prog_diff.values()))
                curr_root = random.randrange(len(ns.notes_array) - 1)
                for c in range(len(curr_ch)):
                    if ns.notes_array[c] in ns.equal_notes.values() and random.randrange(1, 2) == 2:
                        note = [k for k, v in ns.equal_notes.items() if v == note][0]
                    else: note = ns.notes_array[(curr_root + curr_ch[c]) % len(ns.notes_array)] + ' '
                    chord_string += note
                chord_string += "| "
            curr_piece.write(f"{chord_string[:-2]}")

def clear_files():
    confirm = input("Enter 'y' to delete all files in collection directory: \n> ")
    if confirm.upper() == 'Y':
        for path in os.scandir("collection"):
            if path.is_file(): os.remove(path)


#gen_files(2)
#A C# E | C E G | A# D F# G# | F G# B D | F G A