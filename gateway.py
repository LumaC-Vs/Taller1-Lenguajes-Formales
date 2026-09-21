from functions import subset_construction, run_dfa, minimizar_dfa, parsear_formato_texto, estados_equivalentes

def convert_nfa_to_dfa(nfa_data):
    try:
        return subset_construction(nfa_data)
    except Exception as e:
        return {"error": str(e)}

def simulate_dfa(sim_data):
    try:
        return run_dfa(sim_data)
    except Exception as e:
        return {"error": str(e)}

def get_equivalent_states(dfa_data):
    try:
        return minimizar_dfa(dfa_data)
    except Exception as e:
        return {"error": str(e)}

def procesar_casos_texto(texto):
    try:
        casos = parsear_formato_texto(texto)
        resultados = []
        for dfa in casos:
            pares = estados_equivalentes(dfa)
            pares_texto = [f"{p}-{q}" for (p, q) in pares]
            resultados.append(pares_texto)
        return {"results": resultados}
    except Exception as e:
        return {"error": str(e)}