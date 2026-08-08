from functions import subset_construction, run_dfa

def convert_nfa_to_dfa(nfa_data):
    try:
        return subset_construction(nfa_data)
    except Exception as e:
        return {"error": str(e)} #convertimos el error a texto para enviarlo como JSON

def simulate_dfa(sim_data):
    try:
        return run_dfa(sim_data)
    except Exception as e:
        return {"error": str(e)}
    