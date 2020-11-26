import numpy as np

def get_suspects_pairs(suspects, adjacency_matrix, dead_players):
    """Return the pairs of suspects of a game.

    :param suspects: Array of suspect players.
    :param adjacency_matrix: Matrix of players that have seen each other.
    :param dead_players: Array of players that have been eliminated.
    :return: Array of pairs of non-adjacent points (pairs of suspects).
    """

    if type(suspects) is dict:
        suspects = suspects.keys()

    suspects_pairs = set()
    for suspect in suspects:
        for i in range(len(adjacency_matrix[suspect])):
            if adjacency_matrix[suspect, i] == 0 and i not in dead_players and i != suspect:
                suspects_pairs.add((min(i, suspect), max(i, suspect)))
    suspects_pairs = sorted(suspects_pairs, key = lambda x: (x[0], x[1]))
    return suspects_pairs

def get_suspects(adjacency_matrix, dead_players):
    """Compute the suspect with the number of dead players they met.

    :param adjacency_matrix: A two-dimensional numpy matrix representing the adjacency matrix.
    :param dead_players: list of dead players.
    :return: A dictionary containing the suspect with the number of dead players they met.
    :rtype: dict
    """
    suspects = {}
    for dead_player in dead_players:
        for i in range(len(adjacency_matrix[dead_player])):
            if i not in dead_players and adjacency_matrix[dead_player, i] == 1:
                if i in suspects:
                    suspects[i] += 1
                else:
                    suspects[i] = 1
    return suspects


adjacency_matrix = np.array([[0, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
      [0, 1, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
      [1, 0, 0, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
      [0, 1, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
      [0, 0, 0, 1, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 1, 0, 0]])
suspects = get_suspects(adjacency_matrix, [0])
pairs = get_suspects_pairs(suspects, adjacency_matrix, [0])

