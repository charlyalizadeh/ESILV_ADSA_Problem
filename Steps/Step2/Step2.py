from .FindImpostors import  get_suspects, get_suspects_pairs
import numpy as np

def start_step2():
    adjacency_matrix = np.array([[0, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 1, 0, 0]])
    suspects = get_suspects(adjacency_matrix, [0])
    pairs = get_suspects_pairs(suspects, adjacency_matrix, [0])
    for key, val in suspects.items():
        print(key, "is suspect, he met", val, "dead crewmate." if val==1 else "deads crewmates.")
    print("The pairs of suspect are:")
    for pair in pairs:
        print(pair)
