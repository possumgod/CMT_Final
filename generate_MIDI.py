import pretty_midi as pm
from numpy import random as r
import MIDI_properties as mp

'''
generate midi files for testing and the like
'''
INSTRUMENTS_RANGE = 127
TEMPOS = {'Largo': [40, 60], 'Adagio':[60, 72], 'Andante': [72, 84], 
            'Moderato': [85, 110], 'Allegro': [110, 140], 'Presto': [140, 160]}


'''
returns a list of n integers within the range of 0-127 (INSTRUMENT_RANGE), each instrument has the possibility of being a drum
'''
def choose_instruments(num_instr: 'int') -> 'list':
    return [pm.Instrument(program=r.randint(INSTRUMENTS_RANGE), is_drum=r.choice([True, False])) for i in range(num_instr)]

'''
returns randomly selected name and tempo selected from the range
'''
def choose_tempo(tempo_name = '') -> 'tuple':
    tempo_name = r.choice(list(TEMPOS.keys())) if tempo_name not in TEMPOS else tempo_name
    return str(tempo_name), r.randint(TEMPOS[tempo_name][0], TEMPOS[tempo_name][1])

'''
given an overall duration in seconds and number of notes, creates a 2D list with [start, end] times within the 
interval, where the length is the number of notes, durations are randomly assigned based on duration and note #
'''
def note_durations(dur_s: 'int', n: 'int') -> 'list':
    durations = []
    curr_min = 0
    for i in range(n):
        while curr_min < dur_s:
            # logic is a bit funky, but should create dur frame from start of curr window to half, and half to end
            durations.append([r.randint(curr_min, (curr_min + (dur_s / n)))/2,
                                r.randint((curr_min + (dur_s / n))/2, curr_min + (dur_s / n))])
            curr_min += (dur_s / n)
    return durations

'''
returns list of notes length of the number of notes from a given list (from note_durations)
'''
def generate_notes(note_durs: 'int') -> 'list':
    return [r.choice(list(mp.NOTE_VALUES.keys())) for i in range(note_durs)]

'''
returns a randomly populated MIDI file (pm object) with intruments and notes
'''
def assign_instr(m_file=pm.PrettyMIDI(), t='', i_len=r.randint(5, 10), tot_dur=r.randint(10, 50)):
    tempo = choose_tempo(t)
    instruments = choose_instruments(i_len)
    for i in instruments:
        durations = note_durations(tot_dur, len(instruments))
        note_names = generate_notes(len(durations))
        curr_pitch = r.randint(1, 7)
        curr_instr = pm.Instrument(program=i.program)
        
        for note in note_names:
            curr_instr.notes.append(pm.Note(
                                velocity=max(40, min(120, int(160 - tempo[1]/2))),
                                pitch=pm.note_name_to_number(f"{note}{curr_pitch}"), 
                                start=durations[note_names.index(note)][0],
                                end=durations[note_names.index(note)][1]))

        m_file.instruments.append(curr_instr)
    
    return m_file

'''
creates n randomly generated MIDI files in the Collection directory, simply named after the index
'''
def create_collection(n_docs: 'int'):
    for i in range(n_docs):
        assign_instr().write(f'Collection/Piece{i + 1}.mid')


create_collection(2)