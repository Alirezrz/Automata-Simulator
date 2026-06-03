from dfa import DFA, DFATransition
from validator import DFAValidator, ValidationError


class ParseError(Exception):
    """Raised when the raw input cannot be parsed into valid DFA components."""
    pass


class DFABuilder:
    """
    Expected input format:        
        States: q0 q1 q2
        Alphabet: a b
        Start state: q0
        Final states: q2
        Number of transitions: 4
        q0 a q1
        q1 b q2
        q2 a q2
        q2 b q2
    """

    def __init__(self):
        self._validator = DFAValidator()


    def build(self, raw_input):

        states, alphabet, start_state, final_states, raw_transitions = self._parse(raw_input)

        is_valid, errors = self._validator.validate(
            states, alphabet, start_state, final_states, raw_transitions
        )

        if not is_valid:
            self._report_errors(errors)
            return None

        transitions = [
            DFATransition(from_state, symbol, to_state)
            for from_state, symbol, to_state in raw_transitions
        ]

        return DFA(states, alphabet, start_state, final_states, transitions)



    def _parse(self, raw_input):
        
        lines = [line.strip() for line in raw_input.strip().splitlines() if line.strip()]

        states= self._parse_field(lines, "States:")
        alphabet      = self._parse_field(lines, "Alphabet:")
        start_state   = self._parse_single(lines, "Start state:")
        final_states  = self._parse_field(lines, "Final states:")
        n_transitions = self._parse_count(lines, "Number of transitions:")
        transitions   = self._parse_transitions(lines, n_transitions)

        return set(states), set(alphabet), start_state, set(final_states), transitions

    def _parse_field(self, lines, prefix):
        for line in lines:
            if line.lower().startswith(prefix.lower()):
                value = line[len(prefix):].strip()
                if not value:
                    raise ParseError(f"'{prefix}' section is empty.")
                return value.split()
        raise ParseError(f"Missing required section: '{prefix}'")

    def _parse_single(self, lines, prefix):
        values = self._parse_field(lines, prefix)
        
        if len(values) != 1:
            raise ParseError(
                f"'{prefix}' must have exactly one value, got: {values}"
            )
        return values[0]

    def _parse_count(self, lines, prefix):
        values = self._parse_field(lines, prefix)
        if len(values) != 1 or not values[0].isdigit():
            raise ParseError(
                f"'{prefix}' must be a single non-negative integer, got: {values}"
            )
        return int(values[0])

    def _parse_transitions(self, lines, n):

        section_prefixes = (
            "states:", "alphabet:", "start state:",
            "final states:", "number of transitions:",
        )

        transition_lines = [
            line for line in lines
            if not any(line.lower().startswith(p) for p in section_prefixes)
        ]

        if len(transition_lines) < n:
            raise ParseError(
                f"Expected {n} transition(s), but only found {len(transition_lines)}."
            )

        transitions = []
        for line in transition_lines[:n]:
            parts = line.split()
            if len(parts) != 3:
                raise ParseError(
                    f"Invalid transition format: '{line}'. "
                    f"Expected: 'from_state symbol to_state'."
                )
            transitions.append((parts[0], parts[1], parts[2]))

        return transitions


    def _report_errors(self, errors):
        print("\n Invalid DFA — the following error(s) were found:\n")
        for i, error in enumerate(errors, start=1):
            print(f"  {i}. {error}")
        print("\n  ➜  Please fix the above and try again.\n")