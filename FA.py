from graphviz import *
from collections import defaultdict

# a list of all printable ASCII characters
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
           [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
           [chr(i) for i in range(ord('0'), ord('9') + 1)] + \
           ['+', ':', ';', '=', '!', '#', '$', '%', '^', '{', '}',
            '[', ']', '/', '!', '&', '-', '_', '^', '~', '<', '>']
# Special characters
leftBracket = '('
rightBracket = ')'
line = '|'
dot = '.'
star = '*'
epsilon = 'ε'   # will be replaced by '@' in the program since the epsilon character is not on the keyboard


# This class represents a general finite automata from which other classes(NFA and DFA) can be derived from
class FiniteAutomata:
    def __init__(self, symbol):
        self.states = set()     # all states in the finite automaton
        self.symbol = symbol    # input symbol/alphabet
        self.transitions = defaultdict(defaultdict)     # transitions between states
        self.startState = None  # the start state of the finite automaton
        self.finalStates = []   # a list of final states of the FA

    def set_start_state(self, state):     # sets the start state of the FA
        self.startState = state
        self.states.add(state)

    def add_final_state(self, state):     # adds a given state to the list of final states
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalStates:       # add to final state if not already in the list of final states
                self.finalStates.append(s)

    def add_transition(self, from_state, to_state, input_ch):   # Adds transitions between states
        if isinstance(input_ch, str):
            input_ch = set([input_ch])
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state in self.transitions and to_state in self.transitions[from_state]:
            self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(input_ch)
        else:
            self.transitions[from_state][to_state] = input_ch

    def add_transition_dict(self, transitions):  # add transition dictionary  to dictionary
        for from_state, to_states in transitions.items():
            for state in to_states:
                self.add_transition(from_state, state, to_states[state])

    # change states' representing number to start with the given start number
    def new_build_from_number(self, start_num):
        translations = {}
        for i in self.states:
            translations[i] = start_num
            start_num += 1
        new_build = FiniteAutomata(self.symbol)
        new_build.set_start_state(translations[self.startState])
        new_build.add_final_state(translations[self.finalStates[0]])
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                new_build.add_transition(translations[from_state], translations[state], to_states[state])
        return [new_build, start_num]

    def get_epsilon_closure(self, find_state):
        all_states = set()
        states = [find_state]
        while len(states):
            state = states.pop()
            all_states.add(state)
            if state in self.transitions:
                for to_state in self.transitions[state]:
                    if epsilon in self.transitions[state][to_state] and to_state not in all_states:
                        states.append(to_state)
        return all_states

    def get_move(self, state, state_key):   # state_key refers to an alphabet in the symbol
        if isinstance(state, int):
            state = [state]
        traversed_states = set()
        for s in state:
            if s in self.transitions:
                for tns in self.transitions[s]:
                    if state_key in self.transitions[s][tns]:
                        traversed_states.add(tns)
        return traversed_states

    def create(self, fname, pname):    # creates an image of the corresponding FA('png' format)
        automaton = Digraph(pname, filename=fname, format='png')
        automaton.attr(rankdir='LR')

        automaton.attr('node', shape='doublecircle')
        for final_state in self.finalStates:
            automaton.node('s' + str(final_state))

        automaton.attr('node', shape='circle')
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                tmp = ''
                for s in to_states[state]:
                    tmp += s + '|'
                automaton.edge('s' + str(from_state), 's' + str(state), label=tmp[:-1])

        automaton.attr('node', shape='point')
        automaton.edge('', 's' + str(self.startState))
        automaton.render(view=False)


class Regex2NFA:

    def __init__(self, regex):      # constructor
        self.regex = regex
        self.build_nfa()     # builds the NFA

    # create an image of the equivalent NFA of the given regex
    def create_nfa(self):
        self.nfa.create('nfa.gv', 'Non Deterministic Finite Automata')

    @staticmethod
    def get_priority(option):
        if option == line:      # least priority
            return 10
        elif option == dot:
            return 20
        elif option == star:    # highest priority
            return 30
        else:                   # left bracket
            return 0

    @staticmethod
    def basic_struct(input_ch):   # constructs basic NFA. Regex = a -> NFA
        state1 = 1
        state2 = 2
        basic_nfa = FiniteAutomata({input_ch})
        basic_nfa.set_start_state(state1)
        basic_nfa.add_final_state(state2)
        basic_nfa.add_transition(state1, state2, input_ch)
        return basic_nfa

    @staticmethod
    def star_struct(a):  # converting a regex of the form  'a*' to an NFA
        [a, m1] = a.new_build_from_number(2)
        state1 = 1
        state2 = m1
        star_nfa = FiniteAutomata(a.symbol)
        star_nfa.set_start_state(state1)
        star_nfa.add_final_state(state2)
        star_nfa.add_transition(star_nfa.startState, a.startState, epsilon)
        star_nfa.add_transition(star_nfa.startState, star_nfa.finalStates[0], epsilon)
        star_nfa.add_transition(a.finalStates[0], star_nfa.finalStates[0], epsilon)
        star_nfa.add_transition(a.finalStates[0], a.startState, epsilon)
        star_nfa.add_transition_dict(a.transitions)
        return star_nfa

    @staticmethod
    def dot_struct(a, b):    # converting a regex of the form 'a·b' to an  NFA
        [a, m1] = a.new_build_from_number(1)
        [b, m2] = b.new_build_from_number(m1)
        state1 = 1
        state2 = m2 - 1
        dot_nfa = FiniteAutomata(a.symbol.union(b.symbol))
        dot_nfa.set_start_state(state1)
        dot_nfa.add_final_state(state2)
        dot_nfa.add_transition(a.finalStates[0], b.startState, epsilon)
        dot_nfa.add_transition_dict(a.transitions)
        dot_nfa.add_transition_dict(b.transitions)
        return dot_nfa

    @staticmethod
    def line_struct(a, b):   # converting  the form 'a|b' to an NFA
        [a, m1] = a.new_build_from_number(2)
        [b, m2] = b.new_build_from_number(m1)
        state1 = 1
        state2 = m2
        line_nfa = FiniteAutomata(a.symbol.union(b.symbol))
        line_nfa.set_start_state(state1)
        line_nfa.add_final_state(state2)
        line_nfa.add_transition(line_nfa.startState, a.startState, epsilon)
        line_nfa.add_transition(line_nfa.startState, b.startState, epsilon)
        line_nfa.add_transition(a.finalStates[0], line_nfa.finalStates[0], epsilon)
        line_nfa.add_transition(b.finalStates[0], line_nfa.finalStates[0], epsilon)
        line_nfa.add_transition_dict(a.transitions)
        line_nfa.add_transition_dict(b.transitions)
        return line_nfa

    def build_nfa(self):
        symbol = set()
        prev = ''
        transformed_word = ''

        # explicitly add dot to the expression
        for ch in self.regex:
            if ch in alphabet:
                symbol.add(ch)
            if ch in alphabet or ch == leftBracket:
                if prev != dot and (prev in alphabet or prev in [star, rightBracket]):
                    transformed_word += dot
            transformed_word += ch
            prev = ch
        self.regex = transformed_word

        # convert infix expression to postfix expression
        t_word = ''
        stack = []
        for ch in self.regex:
            if ch in alphabet:
                t_word += ch
            elif ch == leftBracket:
                stack.append(ch)
            elif ch == rightBracket:
                while stack[-1] != leftBracket:
                    t_word += stack[-1]
                    stack.pop()
                stack.pop()    # pop left bracket
            else:
                while len(stack) and Regex2NFA.get_priority(stack[-1]) >= Regex2NFA.get_priority(ch):
                    t_word += stack[-1]
                    stack.pop()
                stack.append(ch)
        while len(stack) > 0:
            t_word += stack.pop()
        self.regex = t_word

        # build ε-NFA (epsilon-NFA) from postfix expression
        self.automata = []
        for ch in self.regex:
            if ch in alphabet:
                self.automata.append(Regex2NFA.basic_struct(ch))
            elif ch == line:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.line_struct(a, b))
            elif ch == dot:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.dot_struct(a, b))
            elif ch == star:
                a = self.automata.pop()
                self.automata.append(Regex2NFA.star_struct(a))
        self.nfa = self.automata.pop()
        self.nfa.symbol = symbol


class NFA2DFA:

    def __init__(self, nfa):     #  subset construction technique
        self.build_dfa(nfa)     # takes an NFA object as an argument so that DFA can be constructed from it

    def create_dfa(self):
        self.dfa.create('dfa.gv', 'Deterministic Finite Automata')

    def build_dfa(self, nfa):    # subset construction method
        all_states = dict()  # visited subset
        epsilon_closure = dict()   # every state's ε-closure (epsilon closure)
        state1 = nfa.get_epsilon_closure(nfa.startState)
        epsilon_closure[nfa.startState] = state1
        cnt = 1     # dfa state id
        dfa = FiniteAutomata(nfa.symbol)
        dfa.set_start_state(cnt)
        states = [[state1, dfa.startState]]
        all_states[cnt] = state1
        cnt += 1
        while len(states):
            [state, from_index] = states.pop()
            for ch in dfa.symbol:
                traversed_states = nfa.get_move(state, ch)
                for s in list(traversed_states):
                    if s not in epsilon_closure:
                        epsilon_closure[s] = nfa.get_epsilon_closure(s)
                    traversed_states = traversed_states.union(epsilon_closure[s])
                if len(traversed_states):
                    if traversed_states not in all_states.values():
                        states.append([traversed_states, cnt])
                        all_states[cnt] = traversed_states
                        to_index = cnt
                        cnt += 1
                    else:
                        to_index = [k for k, v in all_states.items() if v == traversed_states][0]
                    dfa.add_transition(from_index, to_index, ch)
            for value, state in all_states.items():
                if nfa.finalStates[0] in state:
                    dfa.add_final_state(value)
            self.dfa = dfa

    def analysis(self, string):     # returns true if the string entered matches with the regex defined.
        string = string.replace('@', epsilon)   # no epsilon sign on the keyboard. Replacing it with the '@' symbol
        current_state = self.dfa.startState
        for ch in string:
            if ch == epsilon:
                continue
            state = list(self.dfa.get_move(current_state, ch))
            if len(state) == 0:
                return False
            current_state = state[0]
        if current_state in self.dfa.finalStates:
            return True
        return False
