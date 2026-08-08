Authors: 
- Luisa María Cuervo Prado.
- Sheryl Astrid Murillo Duque.
  
NFA to DFA Converter

Enviromment:
- Operating System: Windows 11
- Programming Language: Python 3
- Framework: Flask
- Tools: Visual Studio Code, PowerShell
- API Testing: cURL

How to Run?
1. Open a terminal in the project directory.

2. Make sure Python is installed.

3. Install Flask.
pip install flask

4. Start the Flask server with:
python app.py
The server should start at:
http://127.0.0.1:5000

5. To test the NFA to DFA conversion, open another terminal in the proyect and run:
curl.exe -X POST http://localhost:5000/convert -H "Content-Type: application/json" -d "@prueba_profesor.json"
The program wiil read the NFA form prueba_profesor.json , perform the conversion and the return the resulting DFA in JSON format.

6.  To test the DFA simulation, run:
curl.exe -X POST http://localhost:5000/simulate -H "Content-Type: application/json" -d "@prueba_simulate.json"
The program will read the DFA and an input string from `prueba_simulate.json`, and return the path followed and whether the string was accepted.

Algorithm:

The program converst a Non-deterministic Finite Automaton (NFA) into a Deterministic Finite Automaton (DFA) using Subset Construcyion algorithm.

Firts, the program calculates the epsilon-closure of the initial of the DFA.

Then, for each DFA state and for echa symbol in the alphabet, the program:

1. Applies the move operation to find the NFA states reachable using that symbol.
2. Calculates the epsilon-closure of the resulting states.
3. Creates a new DFA state if this set has not been generated before.
4. Adds the corresponding DFA transition.

This process continues until there are no new DFA states to process.

Finally, a DFA state is considered acepting if its set of NFA states contains at least one accepting estae of the original NFA.
