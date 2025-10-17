import V1.note_similarity as ns

# dictionary of the chord progression indexes (compared to notes_array)
# example: C major would be notes_array[0], notes_array[4], notes_array[7] -> C E G
chord_prog_diff = {"MAJOR": [0, 4, 7], "MINOR": [0, 3, 7], "DIMINISHED": [0, 3, 6], "AUGMENTED": [0, 4, 8], "MAJOR7": [0, 4, 7, 11], 
                   "MINOR7": [0, 3, 7, 10], "DOMINANT7": [0, 4, 7, 10], "AUGMENTED7": [0, 4, 8, 10], "DOMINANT7F": [0, 4, 6, 10], 
                   "MINORMAJ7": [0, 3, 7, 11], "HALFDIMINISHED": [0, 3, 6, 10], "DIMINISHED7": [0, 3, 6, 9]}


# prints all chords if no arguments are passed, can pass specific note as a string to print only chords with that as the root
def print_all_chords(ch=""):
    for i in range(len(ns.notes_array)):
        if ch == "" or ch == ns.notes_array[i]:
            print(ns.notes_array[i] + " CHORDS:")
            for chord in chord_prog_diff.keys():
                    c = chord_prog_diff[chord]
                    chord_string = chord + ": - "
                    for j in range(len(c)):
                        chord_string += ns.notes_array[(i + c[j]) % len(ns.notes_array)] + ' '
                    print(chord_string)
            print("\n")

# returns a list that corresponds to the associated value from chord_prog_diff 
def determine_chord(n_seq, c, i=0):
    if i == 0:
        c.append(0)
        determine_chord(n_seq, c, i+1)
    elif i < len(n_seq):
        c.append(c[i - 1] + ns.find_note_dist(n_seq[i], n_seq[i - 1]))
        determine_chord(n_seq, c, i+1)
    return c

# returns the key from chord_prog_diff given a value (assuming there exists a match)
def find_match_chord(chord_n):
    for c_name in chord_prog_diff.keys():
        if determine_chord(chord_n, []) == chord_prog_diff[c_name]:
            return c_name
    return f'NONE ({" ".join(chord_n)})'

# determines if the first chord given is longer than the second to call find_chord_diff, call first
def chord_prog_size(c1, c2):
    return find_chord_diff(c1, c2) if len(c1) <= len(c2) else find_chord_diff(c2, c1)

# first chord len is <= len of the 2nd chord given, takes the difference between each corresponding index
# if the 2nd is longer, it adds the difference bewteen the last index of c1 and the last note of c2
def find_chord_diff(c1, c2):
    c_dist = 0
    for i in range(len(c1)):
        c_dist += abs(c1[i] - c2[i])
    c_dist += (c1[-1] - c1[-2]) if len(c1) != len(c2) else 0
    return c_dist

# calculates the distances from the query chord to each chord in the 'library', adding them to a dictionary
def calc_chord_similarity(collection, query_chord, chord_dists):
    for chord in collection:
        n = ns.find_note_dist(query_chord[0], chord[0])
        c = chord_prog_size(determine_chord(query_chord, []), 
                determine_chord(chord, []))
        curr_chord = find_match_chord(chord)
        chord_dists[f"{chord[0]} {curr_chord}"] = round(ns.euclidian_dist(n, c), 3)
    return chord_dists

# returns a dict in order of the item rank value
def rank_distances(collection_dict):
    return dict(sorted(collection_dict.items(), key=lambda item: item[1]))

def min_chord_weighted(collection, query_sequence):
    min_weight = float('inf')
    best_match = []

    for i in range(len(collection) - len(query_sequence) + 1):
        total_dist = 0
        curr_match = []
        for j in range(len(query_sequence)):
            chord_dists = calc_chord_similarity([collection[j + i]], query_sequence[j], {})
            total_dist += ns.euclidian_mult_weights(chord_dists)
            curr_match.append(collection[i + j])
        
        if min_weight > total_dist:
            min_weight = total_dist
            best_match = curr_match

    return round(min_weight, 3), best_match

def ranking_calc(query_collection, music_f_count):
    ranking = {}
    for i in range(len(query_collection)):
        for j in range(music_f_count):
            collection_text = ns.split_notes(open(f"collection/piece{j + 1}.txt", "r").read())
            query_text = ns.split_notes(query_collection[i])
            #print(f"\nQuery {i + 1}, Document {j + 1}")
            min_dist, best_chords = min_chord_weighted(collection_text, query_text)
            ranking[' | '.join([' '.join(best_chords[i]) for i in range(len(best_chords))])] = min_dist
            #print(f"min dist: {min_dist} \nchords: {' | '.join([' '.join(best_chords[i]) for i in range(len(best_chords))])}")
    return ranking


def rank_return(ranking_dict, p=5, r=2):
    ranked_chords = rank_distances(ranking_dict)
    ranked_w_indexes = [(list(ranking_dict.keys()).index(key), key, value) for key, value in ranked_chords]

    for i, c, d in ranked_w_indexes[:r]:
        if d < p:
            print(f"Document {i + 1}: \nChord: '{c}', distance: {d}")
    return ranked_chords


# TESTING
#ex1_n = ns.find_note_dist("A", "C") #3
#x1_c = chord_prog_size(chord_prog_diff["MAJOR"], chord_prog_diff["MINOR"]) # 1
#print(ex1_n, ex1_c)
#print(ns.euclidian_dist(ex1_n, ex1_c))

'''
#print_all_chords()
print(find_note_dist("D", "A#")) # 4

As_maj = ['A#', 'D', 'F']
G_min = ['G', 'A#', 'D']

print(determine_chord(As_maj, [])) # [0, 4, 7]
print(determine_chord(G_min, [])) # [0, 3, 7]
print(find_note_dist('G', 'A#')) # 3
print(find_note_dist('A#', 'D'))

ex2_n = find_note_dist(G_min[0], As_maj[0]) #2
ex2_c = find_chord_diff(determine_chord(As_maj, []), determine_chord(G_min, []))
print(ex2_n)
print(ex2_c)
print(euclidian_dist(ex2_c, ex2_n))

print(ex1_n)
print(ex1_c)
print(euclidian_dist(ex1_c, ex1_n))
'''