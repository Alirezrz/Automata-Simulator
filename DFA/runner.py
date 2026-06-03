from dfa import DFA, DEAD


class DFARunner:

    def run(self, dfa: DFA, input_string: str) -> bool:

        print(f"\nInput string: {input_string if input_string else '(empty)'}")

        current_state = dfa.start_state
        print(f"Start at state: {current_state}")

        for symbol in input_string:

            if symbol not in dfa.alphabet:
                print(f"Read '{symbol}' -> symbol not in alphabet. String is invalid.")
                print("Result: Rejected")
                print()
                return False

            next_state = dfa.get_next_state(current_state, symbol)
            print(f"Read '{symbol}' -> move from {current_state} to {next_state}")
            current_state = next_state

            if current_state == DEAD:
                print("Entered DEAD state.")
                print("Execution halted early.")
                print("Result: Rejected")
                print()
                return False

        accepted = dfa.is_accepting(current_state)
        print(f"Halted at state: {current_state}")
        print(f"Result: {'Accepted' if accepted else 'Rejected'}")
        print()
        return accepted