# validator.py

from dataclasses import dataclass


@dataclass
class ValidationError:
    rule:str
    message:str

    def __str__(self):
        return f"[{self.rule}] {self.message}"


class DPDAValidator:

    def validate(self, dpda_dict):
        states= dpda_dict['states']
        input_alphabet= dpda_dict['input_alphabet']
        stack_alphabet= dpda_dict['stack_alphabet']
        start_state= dpda_dict['start_state']
        initial_stack= dpda_dict['initial_stack']
        final_states= dpda_dict['final_states']
        acceptance_mode= dpda_dict['acceptance_mode']
        transitions= dpda_dict['transitions']

        errors =[]

        self._check_start_state(start_state, states, errors)
        self._check_final_states(final_states, states, errors)
        self._check_initial_stack(initial_stack, stack_alphabet, errors)
        self._check_acceptance_mode(acceptance_mode, errors)
        self._check_transitions(transitions, states, input_alphabet, stack_alphabet, errors)
        self._check_determinism(transitions, input_alphabet, errors)
        return len(errors) == 0, errors


    def _check_start_state(self, start_state, states, errors):
        if start_state not in states:
            errors.append(ValidationError(rule="START STATE",message=f"Start state '{start_state}' is not in the states set {states}."))

    def _check_final_states(self, final_states, states, errors):
        for state in final_states:
            if state not in states:errors.append(ValidationError(rule="FINAL STATES",message=f"Final state '{state}' is not in the states set {states}."))

    def _check_initial_stack(self, initial_stack, stack_alphabet, errors):
        if initial_stack not in stack_alphabet:errors.append(ValidationError(rule="INITIAL STACK SYMBOL",message=f"Initial stack symbol '{initial_stack}' is not in the stack alphabet {stack_alphabet}."))

    def _check_acceptance_mode(self, acceptance_mode, errors):
        if acceptance_mode not in ('final', 'empty'):errors.append(ValidationError(rule="ACCEPTANCE MODE",message=f"Acceptance mode '{acceptance_mode}' is invalid. Must be 'final' or 'empty'."))

    def _check_transitions(self, transitions, states, input_alphabet, stack_alphabet, errors):
        for t in transitions:
            from_state=t['from_state']
            input_sym= t['input']
            stack_top   = t['stack_top']
            to_state    = t['to_state']
            push= t['push']

            if from_state not in states:
                errors.append(ValidationError(rule="TRANSITION FROM",message=f"Transition from unknown state '{from_state}' — not in states set."))

            if to_state not in states:
                errors.append(ValidationError(rule="TRANSITION TO",message=f"Transition to unknown state '{to_state}' — not in states set."))

            if input_sym != 'eps' and input_sym not in input_alphabet:
                errors.append(ValidationError(rule="TRANSITION INPUT",message=f"Input symbol '{input_sym}' in transition "f"({from_state}, {input_sym}, {stack_top}) is not in the input alphabet."))  

            if stack_top not in stack_alphabet:
                errors.append(ValidationError(rule="TRANSITION STACK TOP",message=f"Stack symbol '{stack_top}' in transition "f"({from_state}, {input_sym}, {stack_top}) is not in the stack alphabet."))

            if push != 'eps':
                for sym in push:         
                    if sym not in stack_alphabet:
                        errors.append(ValidationError(rule="TRANSITION PUSH",message=f"Push symbol '{sym}' in transition "f"({from_state}, {input_sym}, {stack_top}) → push '{push}' "f"is not in the stack alphabet."))

    def _check_determinism(self, transitions, input_alphabet, errors):
        seen = set()
        for t in transitions:
            key = (t['from_state'], t['input'], t['stack_top'])
            if key in seen:
                errors.append(ValidationError(rule="DETERMINISM",message=f"Duplicate transition for "f"('{t['from_state']}', '{t['input']}', '{t['stack_top']}') — "f"at most one transition per (state, input, stack_top) is allowed."))
            else:
                seen.add(key)

        lambda_keys = {
            (t['from_state'], t['stack_top'])
            for t in transitions if t['input'] == 'eps'
        }
        for t in transitions:
            if t['input']!='eps':
                pair = (t['from_state'], t['stack_top'])
                if pair in lambda_keys:
                    errors.append(ValidationError(rule="DETERMINISM (λ-CONFLICT)",message=f"Transition ({t['from_state']}, '{t['input']}', '{t['stack_top']}') "f"conflicts with an existing λ-transition on the same "f"(state, stack_top) pair — this makes the machine non-deterministic."))

    def _report_errors(self, errors):
        print("\n  Invalid DPDA — the following error(s) were found:\n")
        for i, error in enumerate(errors, start=1):
            print(f"  {i}. {error}")
        print("\n   Please fix the above and try again.\n")