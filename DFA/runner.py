from dfa import DFA, DEAD
from visualizer import DFAVisualizer


class DFARunner:
    def __init__(self):
        self.visualizer = DFAVisualizer()

    def run(self, dfa: DFA, input_string: str) -> bool:
        print(f"\nInput string: {input_string if input_string else '(empty)'}")

        current_state = dfa.start_state
        print(f"Start at state: {current_state}")

        frames = []

        frames.append({
            "current_state":     current_state,
            "active_transition": None,
            "label":             f"Start → {current_state}",
            "result":            None,
        })

        for i, symbol in enumerate(input_string, start=1):
            if symbol not in dfa.alphabet:
                print(f"Read '{symbol}' → symbol not in alphabet. String is invalid.")
                print("Result: Rejected")
                print()
                frames.append({
                    "current_state":     current_state,
                    "active_transition": None,
                    "label":             f"'{symbol}' not in alphabet — invalid input",
                    "result":            "rejected",
                })
                self._save_animation(dfa, input_string, frames)
                return False

            next_state = dfa.get_next_state(current_state, symbol)

            frames.append({
                "current_state":     current_state,
                "active_transition": (current_state, symbol),
                "label":             f"Step {i}: read '{symbol}'  ({current_state} → {next_state})",
                "result":            None,
            })

            print(f"Read '{symbol}' → move from {current_state} to {next_state}")
            current_state = next_state

            # Frame B — arrival at next state
            if current_state == DEAD:
                frames.append({
                    "current_state":     current_state,
                    "active_transition": None,
                    "label":             "Entered DEAD state — execution halted",
                    "result":            "rejected",
                })
                print("Entered DEAD state.")
                print("Execution halted early.")
                print("Result: Rejected")
                print()
                self._save_animation(dfa, input_string, frames)
                return False

            frames.append({
                "current_state":     current_state,
                "active_transition": None,
                "label":             f"Arrived at {current_state}",
                "result":            None,
            })

        accepted = dfa.is_accepting(current_state)
        verdict  = "accepted" if accepted else "rejected"
        frames.append({
            "current_state":     current_state,
            "active_transition": None,
            "label":             f"Halted at {current_state} — {'✓ ACCEPTED' if accepted else '✗ REJECTED'}",
            "result":            verdict,
        })

        print(f"Halted at state: {current_state}")
        print(f"Result: {'Accepted' if accepted else 'Rejected'}")
        print()

        self._save_animation(dfa, input_string, frames)
        return accepted


    def _save_animation(self, dfa: DFA, input_string: str, frames: list):
        try:
            path = self.visualizer.animate(dfa, input_string, frames, fps=1)
            print(f"  ℹ  Animation saved → {path}")
        except Exception as e:
            print(f"  ⚠  Could not save animation: {e}")
            print("     Make sure Pillow is installed:  pip install pillow")