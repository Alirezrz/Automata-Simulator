from parser import DPDAParser, ParseError
from validator import DPDAValidator
from dpda import DPDA, DPDATransition
from simulator import DPDASimulator

BANNER = """
╔══════════════════════════════════════╗
║         DPDA Simulator               ║
║                                      ║
╚══════════════════════════════════════╝
"""

INPUT_GUIDE = """
Enter your DPDA definition 
Format:

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


def collect_input():
    lines = []

    prompts = [
        ("States","  States: "),
        ("Input alphabet", "  Input alphabet: "),
        ("Stack alphabet", "  Stack alphabet: "),
        ("Start state", "  Start state: "),
        ("Initial stack symbol", "  Initial stack symbol: "),
        ("Final states",   "  Final states: "),
        ("Acceptance mode",     "  Acceptance mode (final / empty): "),
    ]

    for prefix, prompt in prompts:
        while True:
            try:
                value = input(prompt).strip()
            except EOFError:
                return ""
            if value:
                lines.append(f"{prefix}: {value}")
                break
            print("    This field cannot be empty. Please try again.")

    while True:
        try:
            n_str = input("  Number of transitions: ").strip()
        except EOFError:
            return ""
        if n_str.isdigit():
            n = int(n_str)
            lines.append(f"Number of transitions: {n_str}")
            break
        print("    Please enter a valid non-negative integer.")

    print("  Enter each transition as:  from_state  input  stack_top  to_state  push")
    print("  (use 'eps' for lambda input or empty push)\n")

    for i in range(n):
        while True:
            try:
                t = input(f"  Transition {i + 1}: ").strip()
            except EOFError:
                return ""
            if len(t.split()) == 5:
                lines.append(t)
                break
            print("     Expected exactly 5 fields. Try again.")

    return "\n".join(lines)


def build_dpda(raw_input):
    parser= DPDAParser()
    validator = DPDAValidator()
    dpda_dict = parser.parse(raw_input)
    is_valid, errors = validator.validate(dpda_dict)

    if not is_valid:
        validator._report_errors(errors)
        return None

    transitions = [
        DPDATransition(
            from_state = t['from_state'],
            input= t['input'],
            stack_top  = t['stack_top'],
            to_state = t['to_state'],
            push  = t['push'],
        )
        for t in dpda_dict['transitions']
    ]
    return DPDA(dpda_dict, transitions)

def run_simulation_loop(simulator, dpda):
    print("\n  DPDA is ready. Enter strings to test (type 'exit' to quit).")
    print("─" * 50)

    while True:
        try:
            user_input = input("\n  String to test or exit to stop: ")
        except EOFError:
            break

        if user_input.strip().lower() == "exit":
            break
        simulator.run(dpda, user_input.strip())


def main():
    print(BANNER)
    print(INPUT_GUIDE)

    simulator = DPDASimulator()

    while True:
        raw_input = collect_input()
        if not raw_input.strip():
            print("  No input provided. Please try again.\n")
            continue

        try:
            dpda = build_dpda(raw_input)
        except ParseError as e:
            print(f"\n  Parse error: {e}")
            print("  Please check the format and try again.\n")
            continue

        if dpda is None:
            retry = input("  Would you like to re-enter the DPDA? (yes/no): ").strip().lower()
            if retry not in ("yes", "y"):
                break
            continue

        print("\n  DPDA built successfully!")
        print(dpda)
        run_simulation_loop(simulator, dpda)
        break


if __name__ == "__main__":
    main()