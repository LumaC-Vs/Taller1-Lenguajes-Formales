def epsilon_closure(states, transiciones):
    closure = set(states)
    stack = list(states)

    while stack:
        estado_actual = stack.pop()

        for t in transiciones:
            es_epsilon = t["symbol"] in ["ε", "epsilon", ""]
            sale_de_estado = t["from"] == estado_actual

            if es_epsilon and sale_de_estado:
                destino = t["to"]
                if destino not in closure:
                    closure.add(destino)
                    stack.append(destino)
    return closure

def move(states, symbol, transiciones):
    resultado = set()
    for t in transiciones:
        sale_de_estado = t["from"] in states 
        mismo_simbolo = t["symbol"] == symbol 

        if sale_de_estado and mismo_simbolo:
            resultado.add(t["to"])

    return resultado
def nombre_estado(conjunto):
    return "".join(str(s) for s in sorted(conjunto))

def subset_construction(nfa_data):
    transiciones = nfa_data["transitions"]
    alfabeto = nfa_data["alphabet"]
    inicial = nfa_data["initial"]
    aceptacion_nfa= set(nfa_data["accepting"])

    estado_inicial_dfa = epsilon_closure({inicial}, transiciones)
    print(f"Estado inicial del DFA (ε-closure de {{{inicial}}}): {nombre_estado(estado_inicial_dfa)}")

    dfa_states = [estado_inicial_dfa]
    sin_procesar = [estado_inicial_dfa]
    dfa_transitions = []

    while sin_procesar:
        T = sin_procesar.pop(0)
        print(f"Procesando estado del DFA: {nombre_estado(T)}")

        for simbolo in alfabeto:
            movido = move(T, simbolo, transiciones)
            U = epsilon_closure(movido, transiciones)

            if len(U) > 0:
                es_nuevo = U not in dfa_states
                print(f" leyendo '{simbolo}' desde {nombre_estado(T)} -> {nombre_estado(U)}"+
                        ("Nuevo estado" if es_nuevo else "Estado existente)"))
                
                if es_nuevo:
                    dfa_states.append(U)
                    sin_procesar.append(U)

                dfa_transitions.append({
                "from": nombre_estado(T),
                "symbol": simbolo,
                "to": nombre_estado(U)
            })
    accepting_states = []
    for T in dfa_states:
        interseccion = T & aceptacion_nfa
        if len(interseccion) > 0:
            accepting_states.append(nombre_estado(T))

    print(f"\nEstados finales del DFA: {[nombre_estado(T) for T in dfa_states]}")

    return{
    "dfaStates": [nombre_estado(T) for T in dfa_states],
    "transitions": dfa_transitions,
    "acceptingStates": accepting_states

}

def run_dfa(sim_data):
    dfa_states = sim_data["dfaStates"]
    transitions = sim_data["transitions"]
    accepting_states = sim_data["acceptingStates"]
    input_string = sim_data["input"]

    estado_actual = dfa_states[0]
    path = [estado_actual]

    print(f"Simulando la cadena '{input_string}' desde el estado inicial: {estado_actual}")

    for simbolo in input_string:
        transicion_encontrada = None
        
        for t in transitions:
            mismo_origen = t["from"] == estado_actual
            mismo_simbolo = t["symbol"] == simbolo
            if mismo_origen and mismo_simbolo:
                transicion_encontrada = t
                break

        if transicion_encontrada is None:
            print(f" leyenndo '{simbolo}' desde {estado_actual}' -> no hay transición, cadena rechazada")
            return {"path" : path, "accepted": False}

        estado_actual = transicion_encontrada["to"]
        path.append(estado_actual)
        print(f" leyendo '{simbolo}' -> {estado_actual}")

    aceptada = estado_actual in accepting_states
    resultado_texto = "aceptada" if aceptada else "rechazada"
    print(f"Fin de la cadena. Estado final: {estado_actual} -> {resultado_texto}")
    return {"path": path, "accepted": aceptada}
    

if __name__ == "__main__":
    nfa_ejemplo = {
        "states": [0,1,2,3,4,5,6,7,8],
        "alphabet": ["a", "b"],
        "initial" : 0,
        "accepting": [8],
        "transitions" : [
            {"from": 0, "symbol": "ε", "to": 1},
            {"from": 0, "symbol": "ε", "to": 3},
            {"from": 1, "symbol": "a", "to": 2},
            {"from": 3, "symbol": "b", "to": 4},
        ]
    }
    print(type(nfa_ejemplo))
    resultado = subset_construction(nfa_ejemplo)
    print(resultado)

    dfa_de_prueba = {
            "dfaStates": ["0137", "247", "8", "58", "68"],
            "transitions": [
                {"from": "0137", "symbol": "a", "to": "247"},
                {"from": "0137", "symbol": "b", "to": "8"},
                {"from": "247", "symbol": "a", "to": "247"},
                {"from": "247", "symbol": "b", "to": "58"},
                {"from": "8", "symbol": "a", "to": "8"},
                {"from": "8", "symbol": "b", "to": "68"},
                {"from": "68", "symbol": "b", "to": "8"},
    ],
            "acceptingStates": ["8", "58", "68"],
            "input": "ab"
        }
    
    resultado_simulacion = run_dfa(dfa_de_prueba)
    print(resultado_simulacion)
