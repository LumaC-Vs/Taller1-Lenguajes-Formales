from flask import Flask, request, jsonify
from gateway import convert_nfa_to_dfa, simulate_dfa


app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    resultado = convert_nfa_to_dfa(data)
    return jsonify(resultado)
@app.route("/simulate", methods =["POST"])

def simulate():
    data = request.get_json()
    resultado = simulate_dfa(data)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True, port=5000)