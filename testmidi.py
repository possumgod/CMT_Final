# https://github.com/craffel/pretty-midi?tab=readme-ov-file

import pretty_midi as pm
import V1.note_similarity as ns

midi_test = pm.PrettyMIDI("GF_Theme.mid")
print(f"estimated tempo: {midi_test.estimate_tempo()}")

for instrument in midi_test.instruments:
    print(pm.program_to_instrument_name(instrument.program))
    #for note in instrument.notes:
     #   print(pm.note_number_to_name(note.pitch))