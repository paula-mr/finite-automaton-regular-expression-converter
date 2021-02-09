def read_file(input_file):
    states = {}
    alphabet = []
    initial_states = []
    final_states = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        states = __process_states(lines[0])
        alphabet = __process_list(lines[1])
        initial_states = __process_list(lines[2])
        final_states = __process_list(lines[3])
        i = 4
        while i < len(lines):
            __process_transitions(lines[i], states)
            i += 1

    return states, alphabet, initial_states, final_states

def __process_transitions(line, states):
    items = line.split(",")
    state = states[items[0].strip()]
    symbol = items[1]
    transitions_to = items[2:len(items)]
    transitions = {}

    for t in transitions_to:
        if state.get(t.strip()):
            state[t.strip()] = __format_sum(state[t.strip()], symbol.strip())
        else:
            state[t.strip()] = symbol.strip()

def __format_sum(item1, item2):
    if item1 == '':
        item1 = 'λ'
    if item2 == '':
        item2 = 'λ'
    if item1 == item2:
        return item1
    return '(' + item1 + '+' + item2 + ')'

def __process_states(line):
    states = {}
    list_states = line.split(",")
    for state in list_states:
        states[state.strip()] = {}
    return states

def __process_list(line):
    collection = []
    symbols = line.split(",")
    for symbol in symbols:
        collection.append(symbol.strip())
    return collection