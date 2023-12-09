"""Wolf, goat and cabbage problem"""
from itertools import permutations

#color metacharacters for coloring output
color_codes ={
    "BLUE": '\x1b[34m',
    "GREEN": '\x1b[32m',
    "RED": '\x1b[31m',
    "RESET": '\x1b[0m'
}
# tuple format: (farmer, goat, cabbage, wolf)
# 1- present, 0- not present
# example state: (1,1,1,0)- farmer, goat and cabbage present on one side of river (legal state)

names = ["Farmer", "Goat", "Cabbage", "Wolf"]

def is_legal(state: tuple[int]) -> bool:
    """Checks whether state is legal"""
    goat_cabbage_conflict = (
        state[1] == state[2] == 1   # goat and cabbage present
        and state[0] == 0           # farmer not present
    )
    goat_wolf_conflict = (
        state[1] == state[3] == 1   # goat and wolf present
        and state[0] == 0           # farmer not present
    )
    return not any((goat_cabbage_conflict, goat_wolf_conflict)) # if neither conflict occurs state is legal

def move_is_possible(state1: tuple[int], state2: tuple[int]) -> bool:
    """Farmer can take up to 1 object for move from state1 to state2 to be possible"""
    farmer_moved = state1[0] != state2[0]
    moved = 0
    for present1, present2 in zip(state1[1:], state2[1:]):
        moved += 1 if present1 != present2 else 0
    max_one_object_moved = moved <= 1
    return farmer_moved and max_one_object_moved

def second_side(state: tuple[int]) -> tuple[int]:
    """Returns inverted state tuple (0 <-> 1 inversion) representing second side of river
    
    eg. (1,1,0,0) -> (0,0,1,1)"""
    return tuple(abs(x-1) for x in state)

def game_graph(legal_states: list[tuple[int]]) -> list[tuple[int]]:
    """Creates game graph (list of edges) of possible adjacent states"""
    edges = list()
    for node1, node2 in permutations(legal_states, r= 2):
        if move_is_possible(node1, node2):
            edges.append((node1, node2))

    return edges

def graph_list_to_dict(edges_list: list[tuple[int]]) -> dict:
    """Turns graph represented by list of edges into dictionary listing all node's adjacent nodes"""
    adjacency_dict = dict()
    for edge in edges_list:
        node1, node2 = edge
        adjacency_dict.setdefault(node1, set()).add(node2)

    return adjacency_dict

def find_path(graph: dict[tuple[int]], start: tuple[int], end: tuple[int], path=[]):
    "Finds path from start to end in given graph represented by dictioary of adjacent nodes"
    path = path + [start]
    if start == end:
        return path
    for node in graph[start]:
        if node not in path:
            new_path = find_path(graph, node, end, path)
            if new_path:
                return new_path

    return (start,end,path)

def state_description(state: tuple[int]) -> str:
    """Returns verbal representation of state"""
    state_description_str = str()
    for present, object in zip(state, names):
        state_description_str += object + " " if present else "_" * len(object) + " "

    return state_description_str

def move_description(state1: tuple[int], state2: tuple[int]):
    """Returns description of move done between states"""
    moved_object, direction = str(), str()
    for object, present1, present2 in zip(names, state1, state2):
        if present1 != present2 and object != names[0]:
            moved_object = object
            direction = "right" if present1 else "left"
            break
    if not moved_object:
        moved_object = "alone"
        direction = "right" if state1[0] else "left"

    return f"↓↓↓ Farmer moves {moved_object} to {direction} ↓↓↓"

def path_description(path: list[tuple[int]]):
    """One big formatting clusterfuck; doesnt really matter"""
    description = str()
    for i in range(len(path)-1):
        description += state_description(path[i]) + color_codes["BLUE"] + "∿∿∿∿∿ " + color_codes["RESET"] + state_description(second_side(path[i])) + "\n"
        description += color_codes["RED"] + f"{move_description(path[i], path[i+1]):^55}" + color_codes["RESET"] + "\n" # f"<>:^55" roughly centers move description

    if path[-1] == (0,0,0,0):
        description += state_description(path[-1]) + color_codes["BLUE"] + "∿∿∿∿∿ " + color_codes["RESET"] + state_description(second_side(path[-1])) + "\n"
        description += color_codes["GREEN"] + "••• Success! •••".center(55) + color_codes["RESET"]

    return description

def main():
    string_states = [bin(x)[2:].zfill(4) for x in range(2**4)]      # all possible states in 4-char strings, eg. "1001"
    states = [tuple(map(int, state)) for state in string_states]    # turning all string states into tuples like (1,0,0,1)
    legal_states = [state for state in states if is_legal(state) and is_legal(second_side(state))] # for state to be legal there mustn't be conflict on neither side

    edges = game_graph(legal_states)            # list of edges
    adjacency_dict = graph_list_to_dict(edges)  # dict of neighbours

    path = find_path(adjacency_dict, start=(1,1,1,1), end=(0,0,0,0))

    print(path_description(path))

if __name__ == "__main__":
    main()
