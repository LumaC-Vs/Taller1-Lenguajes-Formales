# NFA to DFA Converter & DFA Minimization

- Luisa María Cuervo Prado
- Sheryl Astrid Murillo Duque

## Environment
- Operating System: Windows 11
- Programming Language: Python 3
- Framework: Flask
- Tools: Visual Studio Code, PowerShell
- API Testing: cURL

## How to Run

1. Open a terminal in the project directory.

2. Make sure Python is installed.

3. Install Flask.

pip install flask


4. Start the Flask server.

python app.py

   The server should start at:

http://127.0.0.1:5000


## Assignment 1 — NFA to DFA Converter

### Endpoint: `POST /convert`
Receives an NFA definition (with optional epsilon transitions) and returns the equivalent DFA, built using the Subset Construction algorithm.

Example call:

curl.exe -X POST http://localhost:5000/convert -H "Content-Type: application/json" -d "@prueba_profesor.json"

The program will read the NFA from `prueba_profesor.json`, perform the conversion, and return the resulting DFA in JSON format.

### Endpoint: `POST /simulate`
Receives an already-built DFA and an input string, and returns the path followed through the DFA and whether the string is accepted.

Example call:

curl.exe -X POST http://localhost:5000/simulate -H "Content-Type: application/json" -d "@prueba_simulate.json"


### Algorithm — Subset Construction
The program converts a Non-deterministic Finite Automaton (NFA) into a Deterministic Finite Automaton (DFA) using the Subset Construction algorithm.

First, the program calculates the epsilon-closure of the initial state to obtain the initial state of the DFA.

Then, for each DFA state and for each symbol in the alphabet, the program:
1. Applies the `move` operation to find the NFA states reachable using that symbol.
2. Calculates the epsilon-closure of the resulting states.
3. Creates a new DFA state if this set has not been generated before.
4. Adds the corresponding DFA transition.

This process continues until there are no new DFA states to process.

Finally, a DFA state is considered accepting if its set of NFA states contains at least one accepting state of the original NFA.

## Assignment 2 — DFA State Minimization

### Endpoint: `POST /equivalent-states`
Receives a DFA using the same JSON convention adopted in Assignment 1 (`states`, `alphabet`, `initial`, `accepting`, `transitions`, with no epsilon transitions), and returns the pairs of equivalent states in lexicographical order.

**Request body example:**
```json
{
  "states": [0, 1, 2, 3, 4, 5],
  "alphabet": ["a", "b"],
  "initial": 0,
  "accepting": [1, 2, 5],
  "transitions": [
    {"from": 0, "symbol": "a", "to": 1},
    {"from": 0, "symbol": "b", "to": 2}
  ]
}
```

**Response example:**
```json
{
  "equivalentStatePairs": ["1-2", "3-4"],
  "totalPairs": 2,
  "minimizedAutomaton": {
    "states": [0, 1, 3, 5],
    "alphabet": ["a", "b"],
    "initial": 0,
    "accepting": [1, 5],
    "transitions": [
      {"from": 0, "symbol": "a", "to": 1},
      {"from": 0, "symbol": "b", "to": 1}
    ]
  }
}
```

Example call:

curl.exe -X POST http://localhost:5000/equivalent-states -H "Content-Type: application/json" -d "@prueba_minimizacion.json"


### Endpoint: `POST /equivalent-states/batch`
Supports the plain-text, multiple-case DFA representation required by the assignment (Section 5.1): a line with the number of cases, followed by, for each case, the number of states, the alphabet, the accepting states, and one transition-table row per state. The initial state is always assumed to be state `0`.

Example call:

curl.exe -X POST http://localhost:5000/equivalent-states/batch -H "Content-Type: text/plain" --data-binary "@prueba_formato_texto.txt"


**Response example:**
```json
{
  "results": [
    ["4-5"]
  ]
}
```

### Algorithm — DFA Minimization (Table-Filling Algorithm)
The program identifies equivalent states in a DFA using the table-filling algorithm presented in Kozen (1997), Lecture 14, based on the construction from Lecture 13.

Two states `p` and `q` are equivalent if and only if, for every string `x`, reading `x` from `p` leads to an accepting state exactly when reading `x` from `q` also leads to an accepting state.

The algorithm works as follows:
1. Build a table containing every unordered pair of distinct states.
2. Mark a pair `{p, q}` if exactly one of the two states is an accepting state.
3. Repeat the following until a full pass produces no new marks: for every unmarked pair `{p, q}`, if there exists a symbol `a` in the alphabet such that the pair `{δ(p, a), δ(q, a)}` is marked, then mark `{p, q}` as well.
4. When no more pairs can be marked, every pair that remains unmarked corresponds to a pair of equivalent states.

### Integration with Assignment 1
The minimization functionality was added directly on top of the existing layered architecture (Controller, Gateway, Functions) from Assignment 1, without modifying any of the original functions:
- `functions.py` gained new functions: `construir_delta` (builds a fast lookup table for the transition function), `estados_equivalentes` (implements the table-filling algorithm), `agrupar_equivalentes` (a Union-Find structure that groups equivalent states together), `construir_automata_minimizado` (builds the fully collapsed DFA from those groups), `minimizar_dfa` (formats the JSON response) and `parsear_formato_texto` (parses the plain-text input format).
- `gateway.py` gained two new functions (`get_equivalent_states` and `procesar_casos_texto`) following the same try/except error-handling pattern used for the Assignment 1 endpoints.
- `app.py` gained two new routes (`/equivalent-states` and `/equivalent-states/batch`), following the same Controller pattern (receive request, delegate to Gateway, return JSON response) used by `/convert` and `/simulate`.

As an additional feature, the response of `/equivalent-states` also includes the fully minimized automaton, obtained by grouping equivalent states with a Union-Find structure and rebuilding the transition table from the resulting groups.