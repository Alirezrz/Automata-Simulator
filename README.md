# DFA Simulator

A clean, educational **Deterministic Finite Automaton (DFA) simulator** written in Python.  
Define any DFA, run test strings through it, and get a full step-by-step execution trace — straight in your terminal.

> 🎨 **Want visualizations?** Check out the [`visualized`](../../tree/visualized) branch — it renders the DFA as a diagram and exports animated GIFs of each simulation, with no system-level dependencies required.

---

## What is a DFA?

A **Deterministic Finite Automaton** is a theoretical model of computation defined by five components:

| Symbol | Name | Description |
|--------|------|-------------|
| Q | States | A finite set of states |
| Σ | Alphabet | A finite set of input symbols |
| δ | Transition function | δ(state, symbol) → next state |
| q₀ | Start state | The state where execution begins |
| F | Final states | States that constitute acceptance |

A string is **accepted** if, after reading every symbol, the machine halts in a final state. Otherwise it is **rejected**.

---

## Features

- ✅ Parse and validate a DFA definition from plain text
- ✅ Detect and report structural problems:
  - Unreachable states (states no input path leads to)
  - Dead states (states from which no accepting state can be reached)
  - Empty language (no string is accepted by the DFA)
- ✅ Auto-complete missing transitions with a `DEAD` trap state
- ✅ Run multiple test strings in one session with a full step-by-step trace
- ✅ Clear, human-readable error messages for invalid DFA definitions

---

## Branches

| Branch | Description |
|--------|-------------|
| `main` | Terminal-only version — no dependencies beyond Python itself |
| [`visualized`](../../tree/visualized) | Adds animated GIF output and a static diagram of the DFA structure |

### What the `visualized` branch adds

- A **static PNG diagram** of the DFA is saved before simulations run
- Each test string produces an **animated GIF** showing the execution step by step:
  - The current state is highlighted in blue
  - The active transition arrow lights up in red as each symbol is read
  - The final state turns **green** (accepted) or **red** (rejected)
- Dependencies (`matplotlib`, `networkx`, `pillow`) are installed automatically on first run — no system-level tools like Graphviz required

---

## Getting Started

### Requirements

- Python 3.10 or higher
- No third-party packages on the `main` branch

### Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

That's it for the terminal version. Run it with:

```bash
python main.py
```

For the visualized version:

```bash
git checkout visualized
python main.py   # missing packages are installed automatically on first run
```

---

## Input Format

When prompted, enter your DFA definition using this format:

```
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
```

Press **Enter on a blank line** when done.

### Format rules

- **States** and **Alphabet** are space-separated values on one line
- **Start state** must be exactly one state from the States list
- **Final states** can be one or more states from the States list
- Each **transition** is on its own line: `from_state symbol to_state`
- The number of transitions and test strings must match the count you declare
- Missing transitions are handled automatically — the simulator adds a `DEAD` trap state for any undefined `(state, symbol)` pair

---

## Example Session

```
╔══════════════════════════════════════╗
║         DFA Simulator                ║
║  Deterministic Finite Automaton      ║
╚══════════════════════════════════════╝

States: q0 q1
Alphabet: a b
Start state: q0
Final states: q0
Number of transitions: 4
q0 a q0
q0 b q1
q1 a q1
q1 b q0
Number of test strings: 3
aab
bb
aba

──────────────────────────────────────────────────
  DFA Analysis
──────────────────────────────────────────────────
     Unreachable states  : none
     Dead states         : none
     Language            : non-empty (at least one string is accepted).
──────────────────────────────────────────────────

  Running simulations...
──────────────────────────────────────────────────

Input string: aab
Start at state: q0
Read 'a' → move from q0 to q0
Read 'a' → move from q0 to q0
Read 'b' → move from q0 to q1
Halted at state: q1
Result: Rejected

Input string: bb
Start at state: q0
Read 'b' → move from q0 to q1
Read 'b' → move from q1 to q0
Halted at state: q0
Result: Accepted

Input string: aba
Start at state: q0
Read 'a' → move from q0 to q0
Read 'b' → move from q0 to q1
Read 'a' → move from q1 to q1
Halted at state: q1
Result: Rejected
```

This DFA accepts strings over `{a, b}` with an **even number of b's**.

---

## Project Structure

```
.
├── main.py          # Entry point — input loop, analysis output, simulation runner
├── dfa.py           # DFA data model (states, alphabet, delta, DEAD state logic)
├── builder.py       # Parses raw text input into a validated DFA object
├── validator.py     # Validates DFA correctness (determinism, state membership, etc.)
├── runner.py        # Executes test strings against the DFA, prints trace
└── visualizer.py    # (visualized branch only) Generates diagrams and animated GIFs
```

---

## Validation Rules

The simulator enforces the formal requirements of a DFA before running any simulation:

1. The start state must belong to the states set
2. All final states must belong to the states set
3. Every transition's source and destination must belong to the states set
4. Every transition symbol must belong to the alphabet
5. No duplicate `(state, symbol)` pairs — a DFA must be deterministic

Any violations are reported clearly with the rule that was broken and what was found.

---

## License

MIT — do whatever you want with it.
