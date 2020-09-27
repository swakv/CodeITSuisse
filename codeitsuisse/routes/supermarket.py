import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

import heapq


def checkBounds(location, board_size_x, board_size_y):
    if location[0] >= board_size_x or location[1] >= board_size_y or location[0] < 0 or location[1] < 0:
        return False
    return True


def graph_construct(arr):

    board_size_x = len(arr)
    board_size_y = len(arr[0])
    graph = {}
    for indx, row in enumerate(arr):
        for indy, elem in enumerate(row):
            if elem == 1:
                continue
            elems = [
                # UP
                (indx-1, indy),
                # DOWN
                (indx+1, indy),
                # LEFT
                (indx, indy-1),
                # RIGHT
                (indx, indy+1)
            ]
            graph[(indx, indy)] = []
            for child in elems:
                if checkBounds(child, board_size_x, board_size_y) and arr[child[0]][child[1]] == 0:
                    graph[(indx, indy)].append(child)
    return graph


def manhattan_dist(location_a, location_b):
    return abs(location_a[0]-location_b[0])+abs(location_a[1]-location_b[1])


def ucs(start_node, goal_node, graph):
    """
    Finds and returns a path, if it exists, between the start node and the goal node.
    """
    timer = 0
    explored = {start_node}
    frontier = []
    cost = 1
    for child_node in graph[start_node]:

        heapq.heappush(
            frontier,
            (
                cost+manhattan_dist(start_node, child_node),
                cost,
                timer,
                child_node,
                [start_node, child_node]
            )
        )
        timer += 1
    while frontier:
        _, g, _, current_node, path = heapq.heappop(frontier)

        if current_node in explored:
            continue
        if current_node == goal_node:
            return len(path)
        explored.add(current_node)

        for child_node in graph[current_node]:

            if child_node not in explored:
                heapq.heappush(
                    frontier,
                    (
                        g+cost+manhattan_dist(current_node, child_node),
                        g+cost,
                        timer,
                        child_node,
                        path+[child_node]
                    )
                )
                timer += 1
    # print(path)
    # print(explored)
    return -1


def handle_case(maze=[[]], start=[0, 0], end=[0, 0]):
    start = tuple(start[::-1])
    end = tuple(end[::-1])
    return ucs(start, end, graph_construct(maze))


def parse(data):
    answers = {}
    for test, case in data["tests"].items():
        answers[test] = handle_case(**case)
    return {"answers": answers}


@app.route('/supermarket', methods=['POST'])
def evaluateSM():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = parse(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
