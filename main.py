''' 
USAGE
DON'T USE: Generate sample collection: main.py -g [num of docs] [min len] [max len]
Clear collection: main.py -g 0
Use query file with precision 5.0: main.py query.txt -p 5
Generate fractal: main.py query.txt -f
'''

# external imports
import argparse
import os
import sys

# imports from other local files
import V1.note_similarity as ns
import V1.chord_similarity as cs
import V1.generate_collection as gc

# contants
music_f_count = 0
for path in os.scandir("collection"):
    if path.is_file():
        music_f_count += 1

# command line args
parser = argparse.ArgumentParser()
parser.add_argument('query', nargs='?')
parser.add_argument('-r', '--recall', type=int, default= 10 if music_f_count > 10 else music_f_count)
parser.add_argument('-p', '--precision', type=float, default=float('inf'))
parser.add_argument('-g', '--generate_files', type=int, nargs='*', default=[5, 5, 15])
parser.add_argument('-f', '--fractal', action='store_true')

def main():
    args = parser.parse_args()
    if args.generate_files is not None and not args.query:
        if args.generate_files[0] == 0:
            gc.clear_files()
        else: gc.gen_files(*args.generate_files)
        sys.exit(0)

    if args.query:
        # first assume is a file
        try:
            query_collection = open(args.query, "r").read().split("\n")
            ra = cs.ranking_calc(query_collection, music_f_count)

            for q_i in range(len(query_collection)):
                print(f"\nQ{q_i + 1}: {query_collection[q_i]}")
                chunk = len(ra) // len(query_collection)
                ranking = cs.rank_return(dict(list(ra.items())[(q_i * chunk):((q_i + 1) * chunk)]), args.precision, args.recall)
                print(ranking)
                
        # if not, assume is a string of notes/chords
        except FileNotFoundError:
            print(f"Results for query {args.query}:\n")
            cs.rank_return(cs.ranking_calc([args.query], music_f_count), args.precision, args.recall)
       
        # else return error
        except Exception as e:
            print(f"Error: {e}")


main()