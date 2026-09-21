from flask import Flask, request, jsonify
from gateway import convert_nfa_to_dfa, simulate_dfa, get_equivalent_states, procesar_casos_texto

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    resultado = convert_nfa_to_dfa(data)
    return jsonify(resultado)

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    resultado = simulate_dfa(data)
    return jsonify(resultado)

@app.route("/equivalent-states", methods=["POST"])
def equivalent_states():
    data = request.get_json()
    resultado = get_equivalent_states(data)
    return jsonify(resultado)

@app.route("/equivalent-states/batch", methods=["POST"])
def equivalent_states_batch():
    texto = request.get_data(as_text=True)
    resultado = procesar_casos_texto(texto)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True, port=5000)