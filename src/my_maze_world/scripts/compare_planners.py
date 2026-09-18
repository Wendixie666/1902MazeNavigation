#!/usr/bin/env python3

import argparse
import csv
import heapq
import time
import tracemalloc
from itertools import count


MAZE = [
    "###############################",
    "#S#       #     #           # #",
    "# # ##### # ### # ######### # #",
    "# #     # #   # #       #   # #",
    "# ##### # ### # ####### # ### #",
    "#     # # #   #     #   #   # #",
    "##### # # # ####### # ##### # #",
    "#     #   #       # #       # #",
    "# ######### ##### # ####### # #",
    "#         #     # #       # # #",
    "# ####### ##### # ####### # # #",
    "#       #     # #       #   # #",
    "####### ##### # ######### ### #",
    "#           #             G   #",
    "###############################",
]


def find_marker(grid, marker):
    for row, line in enumerate(grid):
        for column, value in enumerate(line):
            if value == marker:
                return row, column
    raise ValueError("找不到地图标记: {}".format(marker))


def neighbors(grid, node):
    row, column = node
    for row_delta, column_delta in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        next_row = row + row_delta
        next_column = column + column_delta
        if grid[next_row][next_column] != "#":
            yield next_row, next_column


def search(grid, start, goal, heuristic):
    sequence = count()
    frontier = [(0, next(sequence), start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    closed = set()
    expanded_nodes = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in closed:
            continue

        closed.add(current)
        expanded_nodes += 1
        if current == goal:
            break

        for neighbor in neighbors(grid, current):
            new_cost = cost_so_far[current] + 1
            if new_cost >= cost_so_far.get(neighbor, float("inf")):
                continue
            cost_so_far[neighbor] = new_cost
            came_from[neighbor] = current
            priority = new_cost + heuristic(neighbor, goal)
            heapq.heappush(frontier, (priority, next(sequence), neighbor))

    if goal not in came_from:
        return [], expanded_nodes

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path, expanded_nodes


def dijkstra(grid, start, goal):
    return search(grid, start, goal, lambda _node, _goal: 0)


def a_star(grid, start, goal):
    def manhattan(node, target):
        return abs(node[0] - target[0]) + abs(node[1] - target[1])

    return search(grid, start, goal, manhattan)


def measure(name, planner, grid, start, goal):
    tracemalloc.start()
    start_time = time.perf_counter()
    path, expanded_nodes = planner(grid, start, goal)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": name,
        "path_length": len(path) - 1 if path else None,
        "planning_time_ms": elapsed_ms,
        "expanded_nodes": expanded_nodes,
        "peak_memory_kib": peak_memory / 1024,
        "success": bool(path),
    }


def print_results(results):
    headers = [
        "algorithm",
        "path_length",
        "planning_time_ms",
        "expanded_nodes",
        "peak_memory_kib",
        "success",
    ]
    print("\t".join(headers))
    for result in results:
        print("\t".join(str(result[header]) for header in headers))


def write_csv(path, results):
    with open(path, "w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


def main():
    parser = argparse.ArgumentParser(description="比较 Dijkstra 和 A* 的规划性能")
    parser.add_argument("--csv", help="可选：将结果写入 CSV 文件")
    args = parser.parse_args()

    start = find_marker(MAZE, "S")
    goal = find_marker(MAZE, "G")
    results = [
        measure("Dijkstra", dijkstra, MAZE, start, goal),
        measure("A*", a_star, MAZE, start, goal),
    ]
    print_results(results)
    if args.csv:
        write_csv(args.csv, results)
        print("结果已写入 {}".format(args.csv))


if __name__ == "__main__":
    main()
