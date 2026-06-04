class ParseError(Exception):
    pass
class DPDAParser:
    """
    Expected format:
        States: q0 q1 q2
        Input alphabet: a b
        Stack alphabet: Z A
        Start state: q0
        Initial stack symbol: Z
        Final states: q2
        Acceptance mode: final

        Number of transitions: 4
        q0 a Z q1 AZ
        q1 a A q1 AA
        q1 b A q2 eps
        q2 b A q2 eps
    """

    def parse(self, raw_input):
        lines = [
            line.strip()
            for line in raw_input.strip().splitlines()
            if line.strip() and not line.strip().startswith('#')
        ]

        states = self._parse_field(lines, "States:")
        input_alphabet= self._parse_field(lines, "Input alphabet:")
        stack_alphabet = self._parse_field(lines, "Stack alphabet:")
        start_state  = self._parse_single(lines, "Start state:")
        initial_stack = self._parse_single(lines, "Initial stack symbol:")
        final_states = self._parse_field(lines, "Final states:")
        acceptance_mode= self._parse_single(lines, "Acceptance mode:").lower()
        n_transitions= self._parse_count(lines, "Number of transitions:")
        transitions  = self._parse_transitions(lines, n_transitions)

        return {
            'states' : set(states),
            'input_alphabet': set(input_alphabet),
            'stack_alphabet': set(stack_alphabet),
            'start_state': start_state,
            'initial_stack' : initial_stack,
            'final_states' : set(final_states),
            'acceptance_mode': acceptance_mode,
            'transitions' : transitions,
        }

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
            "states:", "input alphabet:", "stack alphabet:","start state:", "initial stack symbol:","final states:", "acceptance mode:", "number of transitions:",)
        transition_lines = [
            line for line in lines
            if not any(line.lower().startswith(p) for p in section_prefixes)
        ]

        if len(transition_lines)<n:
            raise ParseError(
                f"Expected {n} transition(s), but only found {len(transition_lines)}."
            )

        transitions = []
        for line in transition_lines[:n]:
            parts = line.split()
            if len(parts) != 5:
                raise ParseError(
                    f"Invalid transition format: '{line}'.\n"
                    f"  Expected: from_state  input  stack_top  to_state  push_string"
                )

            from_state, input_sym, stack_top, to_state, push_str = parts

            if input_sym.lower() in ('lambda', 'ε', 'λ','eps'):
                input_sym = 'eps'
            if push_str.lower() in ('lambda', 'ε', 'λ','eps'):
                push_str = 'eps'

            transitions.append({
                'from_state': from_state,
                'input'  : input_sym,
                'stack_top': stack_top,
                'to_state': to_state,
                'push': push_str,
            })

        return transitions