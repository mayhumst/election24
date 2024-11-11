import json
from numpy import random
import matplotlib.pyplot as plt

def sim_election(results, battles, states): 

    # counts the electoral college breakdown of the election 
    fin = {
        "dem": 0, 
        "rep": 0, 
        "unknown": 0, 
        'battles': {
            'Michigan': '',
            'Wisconsin': '',
            'Georgia': '',
            'Nevada': '',
            'North Carolina': '',
            'Arizona': '',
            'Pennsylvania': '',
        }
    }


    # run a simulation on a battleground state based on Siena College polling numbers
    def sim_state(state, fin, results, states, battles):
        
        poll_data = battles[state]["siena_poll"]

        # assuming a margin of error based on a normal distribution, generate a random value for the error and adjust the predicted voting split accordingly
        err = poll_data["margin_err"]
        norm = random.normal(loc=0, scale = err/2, size=2000)
        x = random.choice(norm)

        d = poll_data["dem"]
        r = poll_data["rep"]
        d += x 
        r -= x

        # check who won this state based on new vote percentages
        if d > r:
            """ print("dems win " + state)
            print("d", d, " r", r) """
            fin["battles"][state] = 'd'
            fin["dem"] += states[state]["num_votes"]
            return fin
        if d < r:
            """ print("reps win " + state)
            print("d", d, " r", r) """
            fin["battles"][state] = 'r'
            fin["rep"] += states[state]["num_votes"]
            return fin
        print("somehow, against all odds, the candidates tied")
        fin["battles"][state] = 'u'
        fin["unknown"] += states[state]["num_votes"]
        return fin
    

    # for all fifty states, get the predicted winner
    # for non-battleground states, just use the likely winner
    # for battleground states, run a simulation 
    for state in states.keys():
        # battleground state
        if results[state] == "":
            fin = sim_state(state, fin, results, states, battles)
            continue
        fin[results[state]] += states[state]["num_votes"]
    
    return fin
    

with open("./results.json", 'r') as f:
    results = json.load(f)
with open("./states.json", 'r') as f:
    states = json.load(f)
with open("./battleground.json", 'r') as f:
    battles = json.load(f)

final_results = {
    'total_simulations': 0,
    'total_dems_win': 0, 
    'total_reps_win': 0, 
    'battles': {
        'Michigan': {'d': 0, 'r': 0, 'u': 0},
        'Wisconsin': {'d': 0, 'r': 0, 'u': 0},
        'Georgia': {'d': 0, 'r': 0, 'u': 0},
        'Nevada': {'d': 0, 'r': 0, 'u': 0},
        'North Carolina': {'d': 0, 'r': 0, 'u': 0},
        'Arizona': {'d': 0, 'r': 0, 'u': 0},
        'Pennsylvania': {'d': 0, 'r': 0, 'u': 0},
    }
}

for i in range(0, 2500):
    # run one full election sim 
    x = sim_election(results, battles, states)

    final_results["total_simulations"] += 1

    # determine party winner
    if x["dem"] > x["rep"]:
        final_results["total_dems_win"] += 1
    else:
        final_results["total_reps_win"] += 1
    
    # determine battleground state wins
    for state in final_results["battles"].keys():
        final_results["battles"][state][x["battles"][state]] += 1

# print results / statistics for all simulations
print("")
print("Out of ", final_results["total_simulations"], " simulations:")
print("\trepublicans won ", final_results["total_reps_win"], " elections")
print("\tdemocrats won ", final_results["total_dems_win"], " elections")
print("For each of the seven swing states:")

for statename in final_results["battles"].keys():
    state = final_results["battles"][statename]
    
    print("\t" + statename + ':' + ' '*(15-len(statename)), 'DEM ', state["d"], ' REP ', state["r"], "(TIED " + str(state["u"]) + " time/s)" if state["u"] > 0 else '', ' -- Leans Democrat' if state['d'] > 500 else ' -- Leans Rebublican' if state['r'] > 500 else ' -- No Lean')

