from dataclasses import dataclass


class Stack:
    def __init__(self, initial_symbol):
        self._data = [initial_symbol]

    def top(self):
        return self._data[-1] if self._data else None

    def pop(self):
        return self._data.pop() if self._data else None

    def push(self, symbol):
        self._data.append(symbol)

    def is_empty(self):
        return len(self._data) == 0

    def __str__(self):
        return ''.join(reversed(self._data)) if self._data else '(empty)'

    def __len__(self):
        return len(self._data)

    def copy(self):
        new = Stack.__new__(Stack)
        new._data = self._data.copy()
        return new





@dataclass
class DPDATransition:
    from_state:str
    input  : str  
    stack_top: str  
    to_state : str
    push:str  

    def __repr__(self):
        inp  = 'λ' if self.input == 'eps' else f"'{self.input}'"
        push = 'ε' if self.push  == 'eps' else f"'{self.push}'"
        return (f"δ({self.from_state}, {inp}, {self.stack_top}) "f"-> ({self.to_state}, {push})")


class DPDA:
    """
M = (Q, Σ, Γ, δ, q0, Z0, F)
Attributes:
    states (Q)
    input_alphabet (Σ)
    stack_alphabet(Γ)
    start_state (q0)
    initial_stack(Z0)
    final_states (F)
    acceptance_mode:'final' or 'empty'
    transitions: list of DPDATransition
    delta : dict(from_state, input, stack_top) -> DPDATransition
    """

    def __init__(self, dpda_dict, transitions):
        self.states= dpda_dict['states']
        self.input_alphabet= dpda_dict['input_alphabet']
        self.stack_alphabet= dpda_dict['stack_alphabet']
        self.start_state= dpda_dict['start_state']
        self.initial_stack= dpda_dict['initial_stack']
        self.final_states= dpda_dict['final_states']
        self.acceptance_mode= dpda_dict['acceptance_mode']
        self.transitions = transitions

        self.delta: dict[tuple, DPDATransition] =   {}
        for t in self.transitions:
            key =(t.from_state,t.input, t.stack_top)
            self.delta[key]=t

    def get_transition(self, state, input_sym, stack_top):
        eps_key =(state, 'eps', stack_top)
        if eps_key in self.delta:
            return self.delta[eps_key]

        sym_key = (state, input_sym, stack_top)
        return self.delta.get(sym_key, None)


    def apply_transition(self, stack, transition):
        new_stack = stack.copy()
        new_stack.pop()

        if transition.push !='eps':
            for symbol in reversed(transition.push):
                new_stack.push(symbol)
        return new_stack

    def describe_action(self, transition):
        top  = transition.stack_top
        push = transition.push

        if push == 'eps':
            return f"pop {top}"
        if push == top:
            return f"keep {top}"
        if len(push) > len(top):
            return f"push {push[0]}"
        return f"replace {top} with {push}"

    def is_accepting_final(self, state):
        return state in self.final_states


    def is_accepting_empty(self, stack):
        return len(stack) ==0



    def fresh_stack(self):
        return Stack(self.initial_stack)




    def stack_str(self, stack):
        return ''.join(stack) if stack else '(empty)'
    def __repr__(self):
        return (
            f"DPDA(\n"
            f"  Q   = {self.states}\n"
            f"  Σ   = {self.input_alphabet}\n"
            f"  Γ   = {self.stack_alphabet}\n"
            f"  q0  = {self.start_state}\n"
            f"  Z0  = {self.initial_stack}\n"
            f"  F   = {self.final_states}\n"
            f"  mode= {self.acceptance_mode}\n"
            f"  δ   = {list(self.delta.values())}\n"
            f")"
        )