from builder import DFABuilder, ParseError
from runner import DFARunner


BANNER = """
╔══════════════════════════════════════╗
║         DFA Simulator v1.0           ║
║  Deterministic Finite Automaton      ║
╚══════════════════════════════════════╝
"""

INPUT_GUIDE = """
Enter your DFA definition below.
Format:
  States: (your states here with space)
  Alphabet: (your alphabet here with space)
  Start state: q0 (exp)
  Final states: (your final state/s here (with space))
  Number of transitions: 4      (this is how you should give your transtions based on the example)
  q0 a q1
  q1 b q2
  q2 a q2
  q2 b q2

enter a blank line.
"""


def collect_dfa_input():
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


def run_simulation_loop(runner, dfa):
    print("─" * 45)
    print("  DFA built successfully!")
    print("─" * 45)
    print("  Enter input strings to test. Type 'exit' to quit.")

    while True:
        try:
            user_input = input("\n  Input string: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

        if user_input.lower() == "exit":
            print("\n  Goodbye!")
            break

        runner.run(dfa, user_input)


def main():
    print(BANNER)
    builder = DFABuilder()
    runner  = DFARunner()


    while True:
        raw_input = collect_dfa_input()



        if not raw_input.strip():
            print("  No input provided. Please try again.\n")
            continue

        try:
            dfa = builder.build(raw_input)
        except ParseError as e:
            print(f"\nParse error: {e}")
            print("  Please check the format and try again.\n")
            continue

        if dfa is None:
            retry = input("  Would you like to re-enter the DFA? (yes/no): ").strip().lower()
            if retry not in ("yes", "y"):
                break
            continue

        run_simulation_loop(runner, dfa)
        break


if __name__ == "__main__":
    main()