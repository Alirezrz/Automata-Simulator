import sys
import subprocess

def _ensure_dependencies():
    REQUIRED = {
        "matplotlib": "matplotlib",
        "networkx":   "networkx",
        "PIL":        "pillow",    
    }

    missing = []
    for import_name, pip_name in REQUIRED.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append((import_name, pip_name))

    if not missing:
        return

    print("┌─────────────────────────────────────────────────┐")
    print("│  Missing dependencies detected — installing...  │")
    print("└─────────────────────────────────────────────────┘")
    for import_name, pip_name in missing:
        print(f"  • {pip_name} (import name: {import_name})")
    print()

    for import_name, pip_name in missing:
        print(f"  Installing {pip_name}...", end=" ", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pip_name],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("done ✓")
        else:
            print("FAILED ✗")
            print(f"\n  Could not install '{pip_name}' automatically.")
            print(f"  Please run manually:  pip install {pip_name}")
            print(f"\n  pip error output:\n{result.stderr.strip()}")
            sys.exit(1)

    print("\n  All dependencies installed successfully.\n")

_ensure_dependencies()

from builder import DFABuilder, ParseError
from runner import DFARunner
from dfa import DEAD
from visualizer import DFAVisualizer

BANNER = """
╔══════════════════════════════════════╗
║         DFA Simulator                ║
║  Deterministic Finite Automaton      ║
╚══════════════════════════════════════╝
"""

INPUT_GUIDE = """
Enter your DFA definition below.
Include test strings at the end. Format:

  States: q0 q1 q2
  Alphabet: a b
  Start state: q0
  Final states: q2
  Number of transitions: 4
  q0 a q1
  q1 b q2
  q2 a q2
  q2 b q2
  Number of test strings: 3
  ab
  aba
  bbb

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


def run_simulations(runner, dfa, test_strings):
    print("\n  Running simulations...")
    print("─" * 50)
    for s in test_strings:
        runner.run(dfa, s)


def main():
    print(BANNER)
    builder   = DFABuilder()
    runner    = DFARunner()
    visualizer = DFAVisualizer()

    while True:
        raw_input = collect_input()

        if not raw_input.strip():
            print("  No input provided. Please try again.\n")
            continue

        try:
            dfa, test_strings = builder.build(raw_input)
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

        try:
            import matplotlib.pyplot as plt
            fig, _ = visualizer.generate_graph(dfa)
            fig.savefig("dfa_visualizations/base_structure.png", dpi=120, bbox_inches="tight")
            plt.close(fig)
            print("  Base DFA structural graph saved to dfa_visualizations/base_structure.png")
        except Exception as e:
            print(f"  ⚠  Could not generate base visual graph layout: {e}")

        run_simulations(runner, dfa, test_strings)
        break


if __name__ == "__main__":
    main()