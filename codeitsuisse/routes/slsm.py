import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)



import heapq

def parse(data):
    board_size = data["boardSize"]
    num_players = data["players"]
    jumps = data["jumps"]
    smokes = set()
    mirrors = set()
    snakes = {}
    ladders = {}
    for jump in jumps:
        start, end = jump.split(":")
        start = int(start)
        end = int(end)
        if start == 0:
            mirrors.add(end)
        elif end == 0:
            smokes.add(start)
        elif start > end:
            snakes[start] = end
        else:
            ladders[start] = end
    return {"snakes": snakes, "ladders": ladders, "smokes": smokes,
            "mirrors": mirrors, "board_size": board_size, "num_players": num_players}


# def chutes(snakes=[], ladders=[], smokes=[], mirrors=[], num_players=4, board_size=board_size):
#     pass


def construct_graph(snakes={}, ladders={}, smokes=set(), mirrors=set(), board_size=100, **kwargs):
    states = {}
    for x in range(1, board_size+1):
        states[x] = []
        for roll in range(1, 7):

            if roll+x in snakes:
                states[x].append((roll, snakes[roll+x]))
            elif roll+x in ladders:
                states[x].append((roll, ladders[roll+x]))
            elif roll+x in smokes:
                for second_roll in range(1, 7):
                    states[x].append(((roll, second_roll), roll-second_roll+x))
            elif roll+x in mirrors:
                for second_roll in range(1, 7):
                    if roll+second_roll+x > board_size:
                        new_state = board_size-(roll+second_roll+x-board_size)
                    else:
                        new_state = roll+second_roll+x
                    states[x].append(((roll, second_roll), new_state))
            else:
                if roll+x > board_size:
                    new_state = board_size-(roll+x-board_size)
                else:
                    new_state = roll+x
                states[x].append((roll, new_state))
    return states

# def best_roll


def ucs(start_node, goal_node, graph):
    """
    Finds and returns a path, if it exists, between the start node and the goal node.
    """
    timer = 0
    explored = {start_node}
    frontier = []
    cost = 1
    for action, child_node in graph[start_node]:

        heapq.heappush(
            frontier,
            (
                cost,
                cost,
                timer,
                child_node,
                [action]
            )
        )
        timer += 1
    while frontier:
        _, g, _, current_node, path = heapq.heappop(frontier)

        if current_node in explored:
            continue
        if current_node == goal_node:
            print(g, path)
            return path
        explored.add(current_node)

        for action, child_node in graph[current_node]:

            if child_node not in explored:
                heapq.heappush(
                    frontier,
                    (
                        g+cost,
                        g+cost,
                        timer,
                        child_node,
                        path+[action]
                    )
                )
                timer += 1


# def ucs_subop(start_node, goal_node, graph, min_len):
#     """
#     Finds and returns a path, if it exists, between the start node and the goal node.
#     """
#     timer = 0
#     explored = {start_node}
#     frontier = []
#     cost = 1
#     for action, child_node in graph[start_node]:

#         heapq.heappush(
#             frontier,
#             (
#                 cost,
#                 cost,
#                 timer,
#                 child_node,
#                 [action]
#             )
#         )
#         timer += 1
#     while frontier:
#         _, g, _, current_node, path = heapq.heappop(frontier)

#         if current_node in explored:
#             continue
#         if current_node == goal_node:
#             if len(path) <= min_len:
#                 continue
#             print(g, path)
#             return path
#         explored.add(current_node)

#         for action, child_node in graph[current_node]:

#             if child_node not in explored:
#                 heapq.heappush(
#                     frontier,
#                     (
#                         g+cost,
#                         g+cost,
#                         timer,
#                         child_node,
#                         path+[action]
#                     )
#                 )
#                 timer += 1


def answer(data):
    state_graph = (construct_graph(**parse(data)))
    path = ucs(1, 64, state_graph)
    # path_bad = ucs_subop(1, 64, state_graph, len(path)+1)
    n = data["players"]
    rolls = []
    # if not path:
    #     return [1]*n
    for x in range(len(path)):
        if x < len(path)-1:
            for players in range(n-1):
                if isinstance(path[x], tuple):
                    rolls.append(path[x][0])
                    rolls.append(path[x][1])
                else:
                    rolls.append(path[x])
        else:
            if isinstance(path[x], tuple):
                rolls.append(path[x][0])
                if path[x][1]!= 6:

                    rolls.append(6)
                else:
                    rolls.append(5)
            else:
                if path[x]!= 6:

                    rolls.append(6)
                else:
                    rolls.append(5)
        if isinstance(path[x], tuple):
            rolls.append(path[x][0])
            rolls.append(path[x][1])
        else:
            rolls.append(path[x])
    return rolls


@app.route('/slsm', methods=['POST'])
def evaluateSLSM():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = answer(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
