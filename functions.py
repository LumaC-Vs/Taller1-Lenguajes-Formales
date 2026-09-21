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

def estados_equivalentes(dfa_data):
    estados = dfa_data["states"]
    alfabeto = dfa_data["alphabet"]
    aceptacion = set(dfa_data["accepting"])
    delta = construir_delta(dfa_data["transitions"])

    pares = []
    for i in range(len(estados)):
        for j in range(i + 1, len(estados)):
            pares.append((estados[i], estados[j]))

    marcados = set()
    for (p, q) in pares:
        p_acepta = p in aceptacion
        q_acepta = q in aceptacion
        if p_acepta != q_acepta:
            marcados.add((p, q))

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for (p, q) in pares:
            if (p, q) in marcados:
                continue
            for a in alfabeto:
                p_destino = delta[(p, a)]
                q_destino = delta[(q, a)]
                if p_destino == q_destino:
                    continue
                par_destino = (min(p_destino, q_destino), max(p_destino, q_destino))
                if par_destino in marcados:
                    marcados.add((p, q))
                    hubo_cambio = True
                    break

    equivalentes = [par for par in pares if par not in marcados]
    equivalentes.sort()

    return equivalentes

#Función que agrupa los estados equivalentes
def agrupar_equivalentes(estados, pares_equivalentes):
    padre = {estado: estado for estado in estados}

    def encontrar(x):
        while padre[x] != x:
            x = padre[x]
        return x

    def unir(x, y):
        raiz_x = encontrar(x)
        raiz_y = encontrar(y)
        if raiz_x != raiz_y:
            nueva_raiz = min(raiz_x, raiz_y)
            padre[raiz_x] = nueva_raiz
            padre[raiz_y] = nueva_raiz

    for (p, q) in pares_equivalentes:
        unir(p, q)

    grupos = {}
    for estado in estados:
        grupos[estado] = encontrar(estado)

    return grupos

#
def construir_automata_minimizado(dfa_data):
    estados = dfa_data["states"]
    alfabeto = dfa_data["alphabet"]
    inicial = dfa_data["initial"]
    aceptacion = set(dfa_data["accepting"])
    delta = construir_delta(dfa_data["transitions"])

    pares_equivalentes = estados_equivalentes(dfa_data)
    grupos = agrupar_equivalentes(estados, pares_equivalentes)

    nuevos_estados = sorted(set(grupos.values()))
    nuevo_inicial = grupos[inicial]
    nueva_aceptacion = sorted({grupos[e] for e in aceptacion})

    nuevas_transiciones = []
    for estado in nuevos_estados:
        for simbolo in alfabeto:
            destino_original = delta[(estado, simbolo)]
            destino_nuevo = grupos[destino_original]
            nuevas_transiciones.append({
                "from": estado,
                "symbol": simbolo,
                "to": destino_nuevo
            })

    return {
        "states": nuevos_estados,
        "alphabet": alfabeto,
        "initial": nuevo_inicial,
        "accepting": nueva_aceptacion,
        "transitions": nuevas_transiciones
    }

def minimizar_dfa(dfa_data):
    equivalentes = estados_equivalentes(dfa_data)
    equivalentes.sort()
    pares_texto = [f"{p}-{q}" for (p, q) in equivalentes]

    automata_minimizado = construir_automata_minimizado(dfa_data)

    return {
        "equivalentStatePairs": pares_texto,
        "totalPairs": len(pares_texto),
        "minimizedAutomaton": automata_minimizado
    }
def parsear_formato_texto(texto):
    texto = texto.replace("\r", "")
    lineas = [linea for linea in texto.split("\n") if linea.strip() != ""]
    idx = 0
    num_casos = int(lineas[idx]); idx += 1

    casos = []
    for _ in range(num_casos):
        n = int(lineas[idx]); idx += 1
        alfabeto = lineas[idx].split(); idx += 1
        aceptacion = list(map(int, lineas[idx].split())); idx += 1

        transitions = []
        for estado in range(n):
            fila = list(map(int, lineas[idx].split())); idx += 1
            valores = fila[1:]
            for pos in range(len(alfabeto)):
                simbolo = alfabeto[pos]
                destino = valores[pos]
                transitions.append({"from": estado, "symbol": simbolo, "to": destino})

        dfa = {
            "states": list(range(n)),
            "alphabet": alfabeto,
            "initial": 0,
            "accepting": aceptacion,
            "transitions": transitions
        }
        casos.append(dfa)

    return casos

def construir_delta(transitions):
    delta = {}
    for t in transitions:
        clave = (t["from"], t["symbol"])
        delta[clave] = t["to"]
    return delta

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
    transiciones_ejemplo = [
        {"from": 0, "symbol": "a", "to": 1},
        {"from": 0, "symbol": "b", "to": 2},
        {"from": 1, "symbol": "a", "to": 3},
    ]
    delta_prueba = construir_delta(transiciones_ejemplo)
    print(delta_prueba)
    print(delta_prueba[(0, "a")])

    dfa_minimizacion_2 = {
        "states": [0, 1, 2, 3, 4, 5],
        "alphabet": ["a"],
        "initial": 0,
        "accepting": [1, 4],
        "transitions": [
            {"from": 0, "symbol": "a", "to": 1},
            {"from": 1, "symbol": "a", "to": 2},
            {"from": 2, "symbol": "a", "to": 3},
            {"from": 3, "symbol": "a", "to": 4},
            {"from": 4, "symbol": "a", "to": 5},
            {"from": 5, "symbol": "a", "to": 0},
        ]
    }
    resultado_equiv_2 = estados_equivalentes(dfa_minimizacion_2)
    print(resultado_equiv_2)

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

def construir_delta(transitions):
    delta = {}
    for t in transitions:
        clave = (t["from"], t["symbol"])
        delta[clave] = t["to"]
    return delta
