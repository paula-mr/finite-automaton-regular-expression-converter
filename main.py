import sys
import os

from converter import convert_fa_to_regex

def main(argv):
    input_file = get_startup_arguments(argv)
    states, alphabet, initial_states, final_states = read_file(input_file)
    # print(states)
    result = convert_fa_to_regex(states, alphabet, initial_states, final_states)
    print(result)

def read_file(input_file):
    states = {}
    alphabet = []
    initial_states = []
    final_states = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        states = process_states(lines[0])
        alphabet = process_list(lines[1])
        initial_states = process_list(lines[2])
        final_states = process_list(lines[3])
        i = 4
        while i < len(lines):
            process_transitions(lines[i], states)
            i += 1

    return states, alphabet, initial_states, final_states

def process_transitions(line, states):
    items = line.split(",")
    state = states[items[0].strip()]
    symbol = items[1]
    transitions_to = items[2:len(items)]
    transitions = {}

    for t in transitions_to:
        if state.get(t.strip()):
            state[t.strip()] = state[t.strip()] + '+' + symbol.strip()
        else:
            state[t.strip()] = symbol.strip()

def process_states(line):
    states = {}
    list_states = line.split(",")
    for state in list_states:
        states[state.strip()] = {}
    return states

def process_list(line):
    collection = []
    symbols = line.split(",")
    for symbol in symbols:
        collection.append(symbol.strip())
    return collection

def get_startup_arguments(argv):
    input_file = None

    if len(argv) > 0:
        input_file = argv[0]
    else:
        print('Invalid arguments')
        print("main.py <INPUT FILE>")
        os._exit(1)
    
    return input_file

if __name__ == "__main__":
    main(sys.argv[1:])