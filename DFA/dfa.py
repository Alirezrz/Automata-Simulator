from dataclasses import dataclass

DEAD = "DEAD"


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
        delta        (δ)  — nested dict, includes DEAD state if needed
    """

    def __init__(
        self,
        states: set[str],
        alphabet: set[str],
        start_state: str,
        final_states: set[str],
        transitions: list[DFATransition],
    ):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.final_states = set(final_states)
        self.transitions = list(transitions)

        self.delta: dict[str, dict[str, str]] = {state: {} for state in self.states}
        for t in self.transitions:
            self.delta[t.from_state][t.symbol] = t.to_state

        self._complete_with_dead()

        self._unreachable: set[str] = None
        self._dead_states: set[str] = None



    def _complete_with_dead(self):

        needs_dead = False

        for state in list(self.states):
            for symbol in self.alphabet:
                if symbol not in self.delta[state]:
                    needs_dead = True
                    self.delta[state][symbol] = DEAD

        if needs_dead:
            self.states.add(DEAD)
            self.delta[DEAD] = {symbol: DEAD for symbol in self.alphabet}
            for symbol in self.alphabet:
                self.transitions.append(DFATransition(DEAD, symbol, DEAD))

    def has_dead_state(self):
        return DEAD in self.states



    def get_next_state(self, state, symbol):
        return self.delta.get(state, {}).get(symbol, None)



    def is_accepting(self, state):
        return state in self.final_states



    def get_defined_transitions(self) :
        return self.transitions


    def get_unreachable_states(self):
        if self._unreachable is not None:
            return self._unreachable
        # BFS:
        visited = set()
        queue = [self.start_state]
        visited.add(self.start_state)

        while queue:
            current = queue.pop(0)
            for symbol in self.alphabet:
                nxt = self.get_next_state(current, symbol)
                if nxt and nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)

        self._unreachable = self.states - visited
        return self._unreachable



    def get_dead_states(self):
        if self._dead_states is not None:
            return self._dead_states

        #reverse graph
        reverse: dict[str, set[str]] = {s: set() for s in self.states}
        for state in self.states:
            for symbol in self.alphabet:
                nxt = self.get_next_state(state, symbol)
                if nxt:
                    reverse[nxt].add(state)

        # BFS on reverse graph
        can_reach_accept = set()
        queue = [s for s in self.final_states if s in self.states]
        for s in self.final_states:
            if s in self.states:
                queue.append(s)
                can_reach_accept.add(s)

        while queue:
            current = queue.pop(0)
            for predecessor in reverse.get(current, set()):
                if predecessor not in can_reach_accept:
                    can_reach_accept.add(predecessor)
                    queue.append(predecessor)

        self._dead_states = self.states - can_reach_accept
        return self._dead_states



    def is_language_empty(self) -> bool:
        reachable = self.states - self.get_unreachable_states()
        return len(reachable & self.final_states) == 0

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