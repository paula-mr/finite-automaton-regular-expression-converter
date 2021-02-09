def convert_fa_to_regex(states, alphabet, initial_states, final_states):
    initial_state, final_state, states = __pre_process_fa_to_er(states, initial_states, final_states)
    internal_states = __filter_internal_states(states, initial_state, final_state)
    while len(internal_states) > 0:
        state_e = __choose_state_e_with_lower_pe(internal_states, states)
        states_other_than_e = [state for state in states if state != state_e]
        for state_e1 in states_other_than_e:
            for state_e2 in states_other_than_e:
                s = __get_transition(state_e1, state_e2, states)
                r1 = __get_transition(state_e1, state_e, states)
                r2 = __get_transition(state_e, state_e, states)
                r3 = __get_transition(state_e, state_e2, states)
                if not r1 is None and not r3 is None:
                    states[state_e1][state_e2] = __format_transition(s, r1, r2, r3)
        states.pop(state_e)
        internal_states = __filter_internal_states(states, initial_state, final_state)
    
    regex = states[initial_state][final_state]
    return regex

def __choose_state_e_with_lower_pe(internal_states, states):
    state_e = None
    number_of_transition_states = None
    for state in internal_states:
        states_other_than_e = [state for state in states if state != state_e]
        count_transition_states = 0
        for state_e1 in states_other_than_e:
            for state_e2 in states_other_than_e:
                r1 = __get_transition(state_e1, state, states)
                r3 = __get_transition(state, state_e2, states)
                if not r1 is None and not r3 is None:
                    count_transition_states = count_transition_states + 1
        
        if number_of_transition_states is None or count_transition_states < number_of_transition_states:
            state_e = state
            number_of_transition_states = count_transition_states

    return state_e

def __filter_internal_states(states, initial_state, final_state):
    return [state for state in states if state != initial_state and state != final_state]

def __format_transition(s, r1, r2, r3):
    first_term = __format_parenthesis_term(s) if s is not None else None
    second_term = __format_concat_term(r1) if r1 is not None else None
    third_term = __format_parenthesis_term(r2) if r2 is not None else None
    fourth_term = __format_concat_term(r3) if r3 is not None else None

    result = ''
    if not first_term is None:
        if first_term == '':
            result = 'λ + '
        else:
            result = first_term + ' + '
    
    if not second_term and not third_term and not fourth_term:
        if second_term == '' or third_term == '' or fourth_term == '':
            return result + ' λ'
    
    result = result + second_term if second_term else result
    result = result + third_term + '*' if third_term else result
    result = result + fourth_term if fourth_term else result
    return result

def __format_parenthesis_term(term):
    if term[0] == '(' and term[-1] == ')':
        return term
    return '(' + term + ')'

def __format_concat_term(term):
    if '+' in term and not '(' in term:
        return '(' + term + ')'
    return term

def __get_transition(e1, e2, states):
    return states[e1].get(e2) if states.get(e1) else None

def __pre_process_fa_to_er(states, initial_states, final_states):
    new_initial_state = 'new_i'
    states[new_initial_state] = {}
    
    for state in initial_states:
        states[new_initial_state][state] = ''
                
    new_final_state = 'new_f'
    states[new_final_state] = {}
    
    for state in final_states:
        states[state][new_final_state] = ''
    
    return new_initial_state, new_final_state, states
            