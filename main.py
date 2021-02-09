import sys
import os

from file_decoder import read_file
from converter import RegularExpressionConverter

def main(argv):
    input_file = get_startup_arguments(argv)
    states, alphabet, initial_states, final_states = read_file(input_file)
    converter = RegularExpressionConverter(states, initial_states, final_states, alphabet)
    result = converter.convert()
    print(result)

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