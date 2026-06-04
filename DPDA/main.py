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
Enter your DPDA definition below.
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


def build_dpda(raw_input):
    
    parser    = DPDAParser()
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
            stack_top = t['stack_top'],
            to_state= t['to_state'],
            push = t['push'],
        )
        for t in dpda_dict['transitions']
    ]
    return DPDA(dpda_dict, transitions)


def run_simulation_loop(simulator, dpda):
    print("\n  DPDA is ready. Enter strings to test (type 'exit' to quit, press Enter for empty string).")
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