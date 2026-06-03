from dataclasses import dataclass
@dataclass
class ValidationError:
    rule: str
    message: str
    def __str__(self):
        return f"[{self.rule}] {self.message}"


class DFAValidator:
    """
    Checks:
      1. Start state must be in states set
      2. All final states must be in states set
      3. Each transition's from_state must be in states set
      4. Each transition's to_state must be in states set
      5. Each transition's symbol must be in alphabet
      6. No duplicate (state, symbol) pairs — DFA determinism rule
    """

    def validate(
        self,
        states: set[str],
        alphabet: set[str],
        start_state: str,
        final_states: set[str],
        transitions: list[tuple[str, str, str]],  # (from_state, symbol, to_state)
    ):

        errors: list[ValidationError] = []

        self._check_start_state(start_state, states, errors)
        self._check_final_states(final_states, states, errors)
        self._check_transitions(transitions, states, alphabet, errors)

        is_valid = len(errors) == 0
        
        return is_valid, errors


    def _check_start_state(
        self,
        start_state: str,
        states: set[str],
        errors: list[ValidationError],
    ):
        if start_state not in states:
            errors.append(ValidationError(
                rule="START STATE",
                message=f"Start state '{start_state}' is not in the states set {states}.",
            ))

    def _check_final_states(
        self,
        final_states: set[str],
        states: set[str],
        errors: list[ValidationError],
    ):
        for state in final_states:
            if state not in states:
                errors.append(ValidationError(
                    rule="FINAL STATES",
                    message=f"Final state '{state}' is not in the states set {states}.",
                ))

    def _check_transitions(
        self,
        transitions: list[tuple[str, str, str]],
        states: set[str],
        alphabet: set[str],
         errors: list[ValidationError],
    ):
        seen: set[tuple[str, str]] = set()
        for from_state, symbol, to_state in transitions:

            if from_state not in states:
                errors.append(ValidationError(
                    rule="TRANSITION FROM",
                    message=f"Transition from unknown state '{from_state}' — not in states set {states}.",
                ))

            if to_state not in states:
                errors.append(ValidationError(
                    rule="TRANSITION TO",
                    message=f"Transition to unknown state '{to_state}' — not in states set {states}.",
                ))

            if symbol not in alphabet:
                errors.append(ValidationError(
                    rule="TRANSITION SYMBOL",
                    message=f"Symbol '{symbol}' in transition ({from_state}, '{symbol}') → {to_state} is not in alphabet {alphabet}.",
                ))

            key = (from_state, symbol)
            if key in seen:
                errors.append(ValidationError(
                    rule="DETERMINISM",
                    message=f"Duplicate transition for ('{from_state}', '{symbol}') — a DFA must have at most one transition per (state, symbol) pair.",
                ))
            else:
                seen.add(key)