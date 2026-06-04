from builder import DFABuilder, ParseError
from runner import DFARunner
from dfa import DEAD


BANNER = """
╔══════════════════════════════════════╗
║         DFA Simulator                ║
║                                      ║
╚══════════════════════════════════════╝
"""

INPUT_GUIDE = """
Enter your DFA definition below.
Format:

  States: q0 q1 q2
  Alphabet: a b
  Start state: q0
  Final states: q2
  Number of transitions: 4
  q0 a q1
  q1 b q2
  q2 a q2
  q2 b q2

When finished, press Enter on a blank line.
"""


def collect_input():
    print(INPUT_GUIDE)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


def print_analysis(dfa):
    separator = "─" * 50
    print(separator)
    print("  DFA Analysis")
    print(separator)

    unreachable = dfa.get_unreachable_states()
    unreachable_display = unreachable - {DEAD}
    if unreachable_display:
        states_str = ", ".join(sorted(unreachable_display))
        print(f"  ⚠  Unreachable states  : {{{states_str}}}")
        print(    "     (These states can never be reached from the start state.)")
    else:
        print("     Unreachable states  : none")

    dead_states = dfa.get_dead_states()
    dead_display = dead_states - {DEAD}
    if dead_display:
        states_str = ", ".join(sorted(dead_display))
        print(f"  ⚠  Dead states         : {{{states_str}}}")
        print(    "     (From these states no accepting state can be reached.)")
    else:
        print("     Dead states         : none")

    if dfa.has_dead_state():
        print(f"     DEAD state added   : undefined transitions redirected to '{DEAD}'.")
        print(f"     δ(DEAD, x) = DEAD  for all x ∈ Σ")

    if dfa.is_language_empty():
        print("  ⚠  Language            : EMPTY — no string is accepted by this DFA.")
    else:
        print("     Language            : non-empty (at least one string is accepted).")

    print(separator)


def run_simulation_loop(runner, dfa):
    print("\n  DFA is ready. Enter strings to test (type 'exit' to quit, press Enter for empty string).")
    print("─" * 50)
    while True:
        try:
            user_input = input("\n  String to test or exit to stop: ")
        except EOFError:
            break

        if user_input.strip().lower() == "exit":
            break

        runner.run(dfa, user_input)


def main():
    print(BANNER)
    builder = DFABuilder()
    runner = DFARunner()

    while True:
        raw_input = collect_input()

        if not raw_input.strip():
            print("  No input provided. Please try again.\n")
            continue

        try:
            dfa = builder.build(raw_input)
        except ParseError as e:
            print(f"\n  Parse error: {e}")
            print("  Please check the format and try again.\n")
            continue

        if dfa is None:
            retry = input("  Would you like to re-enter the DFA? (yes/no): ").strip().lower()
            if retry not in ("yes", "y"):
                break
            continue

        print("\n  DFA built successfully!")
        print_analysis(dfa)
        run_simulation_loop(runner, dfa)
        break


if __name__ == "__main__":
    main()