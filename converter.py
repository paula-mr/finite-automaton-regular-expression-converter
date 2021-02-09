class RegularExpressionConverter:
    def __init__(self, states, initial_states, final_states, alphabet):
        self.alphabet = alphabet
        self.initial_state, self.final_state, self.states = self.__pre_process_initial_and_final_states(states, initial_states, final_states)

    def convert(self):
        internal_states = self.__filter_internal_states()
        while len(internal_states) > 0:
            state_e = self.__choose_state_e_with_lower_pe(internal_states)
            states_other_than_e = self.__filter_states_other_than_e(state_e)
            for state_e1 in states_other_than_e:
                for state_e2 in states_other_than_e:
                    self.__process_state(state_e, state_e1, state_e2)
            self.states.pop(state_e)
            internal_states = self.__filter_internal_states()
        
        return self.states[self.initial_state][self.final_state]

    def __filter_internal_states(self):
        return [state for state in self.states if state != self.initial_state and state != self.final_state]

    def __filter_states_other_than_e(self, state_e):
        return [state for state in self.states if state != state_e]

    def __pre_process_initial_and_final_states(self, states, initial_states, final_states):
        new_initial_state = 'new_i'
        states[new_initial_state] = {}
        
        for state in initial_states:
            states[new_initial_state][state] = ''
                    
        new_final_state = 'new_f'
        states[new_final_state] = {}
        
        for state in final_states:
            states[state][new_final_state] = ''
        
        return new_initial_state, new_final_state, states

    def __choose_state_e_with_lower_pe(self, internal_states):
        state_e = None
        number_of_transition_states = None
        for state in internal_states:
            states_other_than_e = self.__filter_states_other_than_e(state_e)
            count_transition_states = 0
            for state_e1 in states_other_than_e:
                for state_e2 in states_other_than_e:
                    r1 = self.__get_transition(state_e1, state)
                    r3 = self.__get_transition(state, state_e2)
                    if not r1 is None and not r3 is None:
                        count_transition_states = count_transition_states + 1
            
            if number_of_transition_states is None or count_transition_states < number_of_transition_states:
                state_e = state
                number_of_transition_states = count_transition_states
            elif count_transition_states == number_of_transition_states and state < state_e:
                state_e = state

        return state_e

    def __process_state(self, state_e, state_e1, state_e2):
        s = self.__get_transition(state_e1, state_e2)
        r1 = self.__get_transition(state_e1, state_e)
        r2 = self.__get_transition(state_e, state_e)
        r3 = self.__get_transition(state_e, state_e2)
        if not r1 is None and not r3 is None:
            self.states[state_e1][state_e2] = self.__format_transition(s, r1, r2, r3)

    def __format_transition(self, s, r1, r2, r3):
        first_term = s if s is not None else None
        second_term = r1 if r1 else ''
        third_term = r2 if r2 is not None else None
        fourth_term = r3 if r3 else ''

        first_half = None
        if not first_term is None:
            if first_term == '':
                first_half = 'λ'
            else:
                first_half = first_term
        
        if not second_term and not third_term and not fourth_term:
            if second_term == '' or third_term == '' or fourth_term == '':
                return self.__format_sum(first_half, 'λ')
        
        second_half = second_term
        second_half = second_half + self.__format_parenthesis(third_term) + '*' if third_term else second_half
        second_half = second_half + fourth_term
        return self.__format_sum(first_half, second_half)

    def __format_sum(self, term1, term2):
        if not term1 and not term2:
            return None
        if term1 and not term2:
            return term1
        if term2 and not term1:
            return term2
        if term1 == term2:
            return term1
        return '(' + self.__format_complex_terms(term1) + '+' + self.__format_complex_terms(term2) + ')'

    def __format_complex_terms(self, term):
        if '+' in term or '*' in term or '(' in term:
            return ' (' + term + ') '
        return term

    def __format_parenthesis(self, term):
        if term[0] == '(' and term[-1] == ')':
            return term
        return '(' + term + ')'

    def __get_transition(self, e1, e2):
        return self.states[e1].get(e2) if self.states.get(e1) is not None else None
            