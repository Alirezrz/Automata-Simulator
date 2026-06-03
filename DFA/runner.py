from dfa import DFA


class DFARunner:
    """
    Simulates a DFA on an input string and prints a step-by-step trace.
    """

    def run(self, dfa: DFA, input_string: str) -> bool:
        """
            True if accepted, False if rejected.
        """
        self._print_header(input_string)

        current_state = dfa.start_state
        print(f"  Step 0 : State = {current_state}  |  Remaining input = \"{input_string}\"")

        for step, symbol in enumerate(input_string, start=1):
            next_state = dfa.get_next_state(current_state, symbol)
            remaining  = input_string[step:]

            if next_state is None:
                print(
                    f"  Step {step} : δ({current_state}, '{symbol}') → ✗  "
                    f"No transition defined — machine is stuck."
                )
                self._print_footer(state=current_state, accepted=False, stuck=True)
                return False

            print(
                f"  Step {step} : δ({current_state}, '{symbol}') → {next_state}"
                f"  |  Remaining input = \"{remaining}\""
            )
            current_state = next_state

        accepted = dfa.is_accepting(current_state)
        self._print_footer(state=current_state, accepted=accepted)
        return accepted


    def _print_header(self, input_string):
        label = f'  Running DFA on input: "{input_string}"  '
        line  = "━" * len(label)
        print(f"\n{line}\n{label}\n{line}")

    def _print_footer(self, state, accepted, stuck = False):
        line = "━" * 45
        print(line)

        if stuck:
            print(f"  Final state : {state}  →  stuck (no valid transition)")
            print(f"  Result      : ✗  REJECTED\n")
        elif accepted:
            print(f"  Final state : {state}  →  {state} ∈ F  ✓")
            print(f"  Result      : ✓  ACCEPTED\n")
        else:
            print(f"  Final state : {state}  →  {state} ∉ F  ✗")
            print(f"  Result      : ✗  REJECTED\n")