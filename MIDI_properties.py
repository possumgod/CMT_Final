import pretty_midi as pm
import math
import collections
from dataclasses import dataclass

'''
Note class:
    note: pitch class note
    accidental: #, b, ''
    octave: specific octave of note
    duration: seconds (to 3 places) of note
'''
@dataclass
class Note:
    note: str
    accidental: str
    octave: int
    duration: float

# stores distances from C to each base note, for example, it takes 2 'steps' to go from C to D
NOTE_VALUES = { 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

# collection and query files used for testing
COLLECTION_TEST = pm.PrettyMIDI("GF_Theme.mid")
QUERY_TEST = pm.PrettyMIDI("UT_Determination.mid")


#####################


'''
adds every note in a given MIDI file to an array by using a dataclass, saves the note, accidental (if it exists), octave, and duration
'''
def notes_details(instrument: 'pm.Instrument', collection_added: 'list'):
    for note in instrument.notes:
        curr_note = list(pm.note_number_to_name(note.pitch))
        collection_added.append(Note(curr_note[0], curr_note[1] if len(curr_note) == 3 else '',     # pitch, accidental
                                    int(curr_note[2] if len(curr_note) == 3 else curr_note[1]),     # octave
                                        round(float(note.end - note.start), 3)))                    # duration
    return collection_added

'''
populates a dictionary with notes, stored according to each instrument in the given MIDI file
ex: {['Lead 1 (square)']: [Note('G', '', 2, 1.2), Note('A', '', 2, 1.4))]}
'''
def generate_note_dict(midi_file):
    midi_dict = {}
    for instrument in midi_file.instruments:
        midi_dict[pm.program_to_instrument_name(instrument.program)] = notes_details(instrument, [])
    
    return midi_dict

# difference in estimated tempo between two MIDI files
def tempo_difference(query_file, collection_file):
    return abs(query_file.estimate_tempo() - collection_file.estimate_tempo())

'''
the total instrumment similarity is calculated based on how much overlap there is between instruments names (by chars)
this is then normalized by dividing the total similarity (tot_sim) by the sqrt of the sum of instruments squared
the higher this value, the more similar the instrument names are, 1 being the highest.
instrument_similarity returns a dictionary with each similarity vlaue and the intruments assigned to those values
'''
def instrument_similarity(query_instrmts: 'pm.PrettyMIDI', collection_instrmts: 'pm.PrettyMIDI'):
    j = 0
    max_sim = 0
    similarities = {}

    qi = query_instrmts.instruments
    ci = collection_instrmts.instruments
    min_instrument = qi if len(qi) < len(ci) else ci
    max_instrument = ci if len(qi) < len(ci) else qi

    for i in range(len(min_instrument)):
        qi_name = pm.program_to_instrument_name(min_instrument[i].program)
        ci_name = pm.program_to_instrument_name(max_instrument[j].program)
        overlap = set((qi_name).split()) & set(ci_name.split())
        tot_sim = len(overlap) / (len(qi_name.split()) + len(ci_name.split()) - len(overlap))

        if tot_sim > max_sim:
            max_sim = tot_sim
            similarities[max_sim] = [min_instrument[i], max_instrument[j]]
            j += 1

    return collections.OrderedDict(similarities)

'''
finds the distance between two notes based on:
    - the abstract values of the integer values of the note pitch classes (see NOTE_VALUES at top)
    - subtracting 1 based on accidental
'''
def semitone_distance(n1: 'Note', n2: 'Note') -> 'int':
    n1_val = NOTE_VALUES[n1.note] + (1 if n1.accidental == '#' else -1 
                                     if n1.accidental == 'b' else 0)
    n2_val = NOTE_VALUES[n2.note] + (1 if n2.accidental == '#' else -1 
                                     if n2.accidental == 'b' else 0)
    
    return min((n2_val - n1_val) % 12, (n1_val - n2_val) % 12)

'''
finds the distance an array of query notes (qn) is from a collection (cn),
returns the closest sequence and the standardized euclidian distance
qn or cn comes from the dict from generate_note_dict for any given instrument (key)
'''
def sequence_distance(qn: "list['Note']", cn: "list['Note']") -> tuple['float', 'list']:
    min_weight = float('inf')
    best_match = []

    for c in range(len(cn) - len(qn) + 1):
        total_dist = 0
        curr_match = []
        for q in range(len(qn)):
            note_dist = semitone_distance(cn[c + q], qn[q])
            total_dist += note_dist**2
            curr_match.append(cn[c + q])

        if min_weight > math.sqrt(total_dist):
            min_weight = math.sqrt(total_dist)
            best_match = curr_match

    return round(min_weight, 3), best_match

'''
given a query and collection MIDI objects, calculates the total similarity across all intruments
'''
def rank_instruments(query: 'pm.PrettyMIDI', collection: 'pm.PrettyMIDI'):
    instrument_total = 0
    instrmt_similarity = instrument_similarity(query, collection)
    for instrmt in instrmt_similarity.keys():
        query_intrmt = generate_note_dict(query)[
            pm.program_to_instrument_name(instrmt_similarity[instrmt][0].program)]
        collection_intrmt = generate_note_dict(collection)[
            pm.program_to_instrument_name(instrmt_similarity[instrmt][1].program)]
        instrument_total += math.pow(sequence_distance(query_intrmt[:20], collection_intrmt)[0], 2)
    return math.sqrt(instrument_total)

def rank_collection(query: "list['Note']"):
    return

# TESTING
test_collection_intrmts = [instrument for instrument in COLLECTION_TEST.instruments]
test_query_intrmts = [instrument for instrument in QUERY_TEST.instruments]

instrmt_similarity = instrument_similarity(QUERY_TEST, COLLECTION_TEST) #FDFFDG vs FDADFD
#print(generate_note_dict(COLLECTION_TEST)[pm.program_to_instrument_name(instruments[1].program)])
print(rank_instruments(QUERY_TEST, COLLECTION_TEST))
#print(ri_test)

#print(instrument_similarity(test_query_intrmts, test_collection_intrmts))
#print(f"#### \n{semitone_distance(Note('C', '', 2, 1.2), Note('B', '', 2, 1.4))}")

#sprint(sequence_distance([Note('B', 'b', 2, 1.2), Note('F', '#', 2, 1.4)],
         #[Note('E', 'b', 2, 1.2), Note('A', '', 2, 1.4), Note('B', '', 2, 1.2), Note('A', '', 2, 1.4)]))