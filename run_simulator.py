import subprocess
import sys

BANNER = """
╔══════════════════════════════════════╗
║         DFA & DPDA Simulator         ║
║                                      ║
╚══════════════════════════════════════╝
"""

print(BANNER)
print("Choose which automaton to simulate:")
print("  1 → DFA")
print("  2 → DPDA")

dfa_choices  = ["1", "dfa"]
dpda_choices = ["2", "dpda"]

while True:
    choice = input("\n  Your choice: ").strip().lower()

    if choice in dfa_choices:
        subprocess.run([sys.executable, "DFA/main.py"])
        break
    elif choice in dpda_choices:
        subprocess.run([sys.executable, "DPDA/main.py"])
        break
    else:
        print("  Invalid choice. Please enter 1 or 2.")