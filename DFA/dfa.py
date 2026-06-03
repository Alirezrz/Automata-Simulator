from dataclasses import dataclass


@dataclass
class DFATransition:
    from_state: str
    symbol: str
    to_state: str

    def __repr__(self):
        return f"δ({self.from_state}, '{self.symbol}') → {self.to_state}"


class DFA:
    """
    M = (Q, Σ, δ, q0, F)
    Attributes:
        states       (Q)  
        alphabet     (Σ)  
        start_state  (q0) 
        final_states (F)  
        delta        (δ) 
    """

    def __init__(
        self,
        states: set[str],
        alphabet: set[str],
        start_state: str,
        final_states: set[str],
        transitions: list[DFATransition],
    ):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions

        self.delta: dict[str, dict[str, str]] = {state: {} for state in states}
        for t in transitions:
            self.delta[t.from_state][t.symbol] = t.to_state


    
    def get_next_state(self, state, symbol):
        return self.delta.get(state, {}).get(symbol, None)





    def is_accepting(self, state):
        return state in self.final_states

    def get_defined_transitions(self):
        return self.transitions

    def __repr__(self):
        return (
            f"DFA(\n"
            f"  Q  = {self.states}\n"
            f"  Σ  = {self.alphabet}\n"
            f"  q0 = {self.start_state}\n"
            f"  F  = {self.final_states}\n"
            f"  δ  = {dict(self.delta)}\n"
            f")"
        )