# Automata Simulator

A clean, educational simulator for two foundational models of computation — **Deterministic Finite Automata (DFA)** and **Deterministic Pushdown Automata (DPDA)** — written in pure Python.

Define any machine, run test strings through it, and get a full step-by-step execution trace straight in your terminal.

---

## What is Simulated?

### Deterministic Finite Automaton (DFA)

A DFA is defined by five components:

| Symbol | Name | Description |
|--------|------|-------------|
| Q | States | A finite set of states |
| Σ | Alphabet | A finite set of input symbols |
| δ | Transition function | δ(state, symbol) → next state |
| q₀ | Start state | The state where execution begins |
| F | Final states | States that constitute acceptance |

A string is **accepted** if, after reading every symbol, the machine halts in a final state.

---

### Deterministic Pushdown Automaton (DPDA)

A DPDA extends the DFA with a stack, giving it the power to recognize context-free languages. It is defined by seven components:

| Symbol | Name | Description |
|--------|------|-------------|
| Q | States | A finite set of states |
| Σ | Input alphabet | A finite set of input symbols |
| Γ | Stack alphabet | A finite set of stack symbols |
| δ | Transition function | δ(state, input, stack\_top) → (next\_state, push\_string) |
| q₀ | Start state | The state where execution begins |
| Z₀ | Initial stack symbol | The symbol placed on the stack at the start |
| F | Final states | States that constitute acceptance (in final state mode) |

A string is accepted either by **reaching a final state** or by **emptying the stack** — the mode is specified as part of the machine definition.

The simulator enforces **determinism**: for every triple `(state, input, stack_top)` at most one transition may be defined. Furthermore, if a λ-transition `δ(q, λ, X)` exists, no symbol transition `δ(q, a, X)` may exist for any `a ∈ Σ`.

---

## Features

### DFA
- ✅ Step-by-step execution trace for every test string
- ✅ Structural analysis after building:
  - Unreachable states
  - Dead states
  - Empty language detection
- ✅ Auto-completes missing transitions with a `DEAD` trap state
- ✅ Clear validation errors for invalid definitions

### DPDA
- ✅ Step-by-step execution trace showing state, symbol read, stack top, action, and stack contents at every transition
- ✅ Supports both **Final State** and **Empty Stack** acceptance modes simultaneously — the decision is made based on the mode declared in the input
- ✅ Full validation including λ-conflict detection and stack alphabet checks
- ✅ Stack displayed top-first at every step

### Both
- ✅ Single entry point `run_simulator.py` to choose between DFA and DPDA at launch
- ✅ Human-readable error messages for every validation rule

---

## Branches

| Branch | Description |
|--------|-------------|
| `main` | Terminal-only, no dependencies beyond Python |
| [`dfa_visualization`](../../tree/dfa_visualization) | Adds static diagram + animated GIF output for DFA simulations |
| [`dpda_visualization`](../../tree/dpda_visualization) | Adds state graph + live stack panel animated GIF output for DPDA simulations |

Both visualization branches generate an animated GIF per test string showing the execution step by step — no system-level tools like Graphviz required.

---

## Getting Started

### Requirements

- Python 3.10 or higher
- No third-party packages on `main`

### Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Run

```bash
python run_simulator.py
```

You will be prompted to choose between DFA and DPDA. The relevant simulator launches immediately.

For a visualization branch:

```bash
git checkout dfa_visualization   # or dpda_visualization
```

---

## Project Structure

```
.
├── run_simulator.py                  # Entry point — choose DFA or DPDA at launch
│
├── DFA/
│   ├── main.py             # Input loop, analysis output, simulation runner
│   ├── dfa.py              # DFA data model (states, alphabet, delta, DEAD state logic)
│   ├── builder.py          # Parses raw text input into a validated DFA object
│   ├── validator.py        # Validates DFA correctness
│   └── runner.py           # Executes test strings, prints trace
│
└── DPDA/
    ├── main.py             # Input loop and simulation runner
    ├── dpda.py             # DPDA data model, Stack class, transition logic
    ├── parser.py           # Parses raw text input into a validated DPDA dict
    ├── validator.py        # Validates DPDA correctness including determinism
    └── simulator.py        # Executes test strings step by step, prints trace
```

---

## Input Format

Both simulators use guided input — you are prompted for each field one at a time with no need to type prefixes.

### DFA example session

```
  States: q0 q1 q2
  Alphabet: a b
  Start state: q0
  Final states: q2
  Number of transitions: 4
  Transition 1: q0 a q1
  Transition 2: q1 b q2
  Transition 3: q2 a q2
  Transition 4: q2 b q2
```

### DPDA example session

```
  States: q0 q1 q2
  Input alphabet: a b
  Stack alphabet: Z A
  Start state: q0
  Initial stack symbol: Z
  Final states: q2
  Acceptance mode (final / empty): final
  Number of transitions: 4
  Transition 1: q0 a Z q1 AZ
  Transition 2: q1 a A q1 AA
  Transition 3: q1 b A q2 eps
  Transition 4: q2 b A q2 eps
```

### DPDA transition format

```
from_state  input  stack_top  to_state  push_string
```

- Use `eps` for a λ (epsilon) input — the transition fires without consuming a symbol
- Use `eps` as the push string to pop without pushing anything
- Push strings are written **top-first**: `AZ` means A ends up on top of Z

---

## Example Output

### DFA

```
Input string: aabb
Start at state: q0
Read 'a' -> move from q0 to q1
Read 'a' -> move from q1 to q1
Read 'b' -> move from q1 to q2
Read 'b' -> move from q2 to q2
Halted at state: q2
Result: Accepted
```

### DPDA

```
Input string: aabb
Acceptance mode: final

State: q0 , Stack: Z
Read a -> push A
State: q1 , Stack: AZ

Read a -> push A
State: q1 , Stack: AAZ

Read b -> pop A
State: q2 , Stack: AZ

Read b -> pop A
State: q2 , Stack: Z

Halted at state: q2
Acceptance mode: final
Result: Accepted
```

---

## Validation Rules

### DFA

1. Start state must belong to Q
2. All final states must belong to Q
3. Every transition's source and destination must belong to Q
4. Every transition symbol must belong to Σ
5. No duplicate `(state, symbol)` pairs — determinism

### DPDA

1. Start state must belong to Q
2. All final states must belong to Q
3. Initial stack symbol must belong to Γ
4. Acceptance mode must be `final` or `empty`
5. Every transition's source and destination must belong to Q
6. Every transition input must belong to Σ or be `eps`
7. Every transition stack top must belong to Γ
8. Every push symbol must belong to Γ
9. No duplicate `(state, input, stack_top)` triples — determinism
10. If `δ(q, λ, X)` is defined, `δ(q, a, X)` must not exist for any `a ∈ Σ` — λ-conflict rule

---

