def convert_fa_to_regex(states, alphabet, initial_states, final_states):
    regex = ''

    __pre_process_fa_to_er(states, initial_states, final_states)
    internal_states = [state for state in states if state not in initial_states and state not in final_states]
    #TODO implement external loop for k until n
    for state_e in internal_states:
        copy_states = [state for state in states]
        for state_e1 in copy_states:
            for state_e2 in copy_states:
                if state_e1 != state_e2:
                    s = __get_transition(state_e1, state_e2, states)
                    r1 = __get_transition(state_e1, state_e, states)
                    r2 = __get_transition(state_e, state_e, states)
                    r3 = __get_transition(state_e, state_e2, states)
                    if not states.get(state_e1):
                        states[state_e1] = {}
                    states[state_e1][state_e2] = __format_transition(s, r1, r2, r3)
        states.pop(state_e)
    
    print(states)

    regex = ''
    return regex

def __format_transition(s, r1, r2, r3):
    result = s + '+' if s else ''
    result = result + r1 if r1 else result
    result = result + r2 + '*' if r2 else result
    result = result + r3 if r3 else result
    return result

def __get_transition(e1, e2, states):
    return states[e1].get(e2) if states.get(e1) else None

def __pre_process_fa_to_er(states, initial_states, final_states):
    if len(initial_states) > 1:
        new_initial_state = 'new_i'
        states[new_initial_state] = {}
        
        for state in initial_states:
            states[new_initial_state][state] = ''
            
    if len(final_states) > 1:
        new_final_state = 'new_f'
        states[new_final_state] = {}
        
        for state in final_states:
            states[state][new_final_state] = ''
            