# -*- coding: utf-8 -*-
# Tìm kiếm và suy luận — chạy các bước như notebook từ trên xuống.

# Bước 1
from collections import deque
import heapq
import math

graph = {
    "S": [("B", 1), ("A", 2)],
    "A": [("G", 2)],
    "B": [("G", 10)],
    "G": [],
}

def path_cost(path):
    total = 0
    for source, target in zip(path, path[1:]):
        total += next(cost for node, cost in graph[source] if node == target)
    return total

def bfs_path(source, target):
    queue = deque([[source]])
    seen = {source}
    while queue:
        path = queue.popleft()
        if path[-1] == target:
            return path
        for node, _ in graph[path[-1]]:
            if node not in seen:
                seen.add(node)
                queue.append(path + [node])
    return None

bfs_answer = bfs_path("S", "G")
print("BFS:", bfs_answer, "chi phí:", path_cost(bfs_answer))

# Bước 2
def astar(source, target, heuristic):
    best_cost = {source: 0}
    parent = {source: None}
    heap = [(heuristic[source], 0, source)]
    expanded = []
    while heap:
        _, cost, node = heapq.heappop(heap)
        if cost != best_cost[node]:       # bỏ mục heap đã lỗi thời
            continue
        expanded.append(node)
        if node == target:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return cost, path[::-1], expanded
        for next_node, edge_cost in graph[node]:
            assert edge_cost >= 0
            candidate = cost + edge_cost
            if candidate < best_cost.get(next_node, math.inf):
                best_cost[next_node] = candidate
                parent[next_node] = node
                priority = candidate + heuristic[next_node]
                heapq.heappush(heap, (priority, candidate, next_node))
    return math.inf, None, expanded

h_good = {"S": 4, "A": 2, "B": 10, "G": 0}
h_zero = {node: 0 for node in graph}
h_bad = {"S": 0, "A": 100, "B": 0, "G": 0}
for name, heuristic in [("Dijkstra", h_zero), ("A*", h_good), ("A* h sai", h_bad)]:
    cost, path, expanded = astar("S", "G", heuristic)
    print(f"{name}: cost={cost}, path={path}, mở={expanded}")

# Bước 3
def exhaustive_cost(source, target, seen=None):
    seen = {source} if seen is None else seen
    if source == target:
        return 0
    candidates = []
    for node, cost in graph[source]:
        if node not in seen:
            tail = exhaustive_cost(node, target, seen | {node})
            candidates.append(cost + tail)
    return min(candidates, default=math.inf)

truth = {node: exhaustive_cost(node, "G") for node in graph}
assert all(0 <= h_good[node] <= truth[node] for node in graph)
assert all(h_good[u] <= cost + h_good[v] for u in graph for v, cost in graph[u])
assert astar("S", "G", h_good)[0] == truth["S"] == 4
violations = [node for node in graph if h_bad[node] > truth[node]]
print("Chi phí còn lại thật:", truth)
print("Heuristic sai vượt lower bound tại:", violations)

# Bước 4
import random

N = 30
START, GOAL = (0, 0), (N - 1, N - 1)

def neighbors(cell, walls):
    r, c = cell
    for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
        if 0 <= nr < N and 0 <= nc < N and (nr, nc) not in walls:
            yield (nr, nc)

def cost_to_goal(walls):                 # BFS ngược từ đích: h* của mọi ô
    dist = {GOAL: 0}
    queue = deque([GOAL])
    while queue:
        cell = queue.popleft()
        for nxt in neighbors(cell, walls):
            if nxt not in dist:
                dist[nxt] = dist[cell] + 1
                queue.append(nxt)
    return dist

def random_map(seed):
    rng = random.Random(seed)
    while True:                          # bốc lại tới khi START tới được GOAL
        walls = {(r, c) for r in range(N) for c in range(N) if rng.random() < 0.3}
        walls -= {START, GOAL}
        dist = cost_to_goal(walls)
        if START in dist:
            return walls, dist

def grid_astar(walls, h, weight=1):
    best = {START: 0}
    heap = [(weight * h(START), 0, START)]
    expanded = 0
    while heap:
        _, cost, cell = heapq.heappop(heap)
        if cost != best[cell]:
            continue
        expanded += 1
        if cell == GOAL:
            return cost, expanded
        for nxt in neighbors(cell, walls):
            if cost + 1 < best.get(nxt, math.inf):
                best[nxt] = cost + 1
                heapq.heappush(heap, (cost + 1 + weight * h(nxt), cost + 1, nxt))
    return math.inf, expanded

def manhattan(cell):
    return abs(cell[0] - GOAL[0]) + abs(cell[1] - GOAL[1])

results = {"Dijkstra": [], "A* Manhattan": [], "A* model": [], "Weighted A* w=2": []}
for seed in range(20):
    walls, dist = random_map(seed)
    rng = random.Random(1000 + seed)
    factor = {cell: rng.uniform(0.7, 1.4) for cell in dist}   # sai số -30% đến +40%
    def model(cell):
        return dist[cell] * factor[cell]
    setups = [("Dijkstra", lambda cell: 0, 1), ("A* Manhattan", manhattan, 1),
              ("A* model", model, 1), ("Weighted A* w=2", manhattan, 2)]
    for name, h, weight in setups:
        cost, expanded = grid_astar(walls, h, weight)
        results[name].append((cost / dist[START], expanded))

for name, rows in results.items():
    ratios = [ratio for ratio, _ in rows]
    longer = sum(ratio > 1 for ratio in ratios)
    mean_expanded = sum(expanded for _, expanded in rows) / len(rows)
    print(f"{name:15s}  dài hơn tối ưu {longer:2d}/20  tệ nhất x{max(ratios):.3f}  "
          f"mở trung bình {mean_expanded:.1f}")
assert max(r for r, _ in results["A* Manhattan"]) == 1
assert max(r for r, _ in results["A* model"]) <= 1.4
assert max(r for r, _ in results["Weighted A* w=2"]) <= 2

# Bước 5
def minimax(tree, maximizing=True):
    if isinstance(tree, (int, float)):
        return tree
    child_values = [minimax(child, not maximizing) for child in tree]
    return max(child_values) if maximizing else min(child_values)

game_tree = [[3, 5], [2, 9]]
branch_values = [minimax(branch, maximizing=False) for branch in game_tree]
print("Giá trị hai nhánh:", branch_values)
print("Minimax:", minimax(game_tree), "chọn A:", branch_values[0] > branch_values[1])
assert minimax(game_tree) == 3

# Bước 6
from itertools import product

variables = ["A", "B", "C"]
edges = [("A", "B"), ("B", "C")]

def consistent(assignment):
    if "A" in assignment and assignment["A"] != 0:
        return False
    for left, right in edges:
        if left in assignment and right in assignment:
            if assignment[left] == assignment[right]:
                return False
    return True

def backtrack(assignment):
    if len(assignment) == len(variables):
        return [assignment.copy()]
    variable = variables[len(assignment)]
    answers = []
    for room in [0, 1]:
        assignment[variable] = room
        if consistent(assignment):
            answers.extend(backtrack(assignment))
        del assignment[variable]
    return answers

csp_answers = backtrack({})
oracle_answers = []
for rooms in product([0, 1], repeat=3):
    A, B, C = rooms
    if A == 0 and A != B and B != C:
        oracle_answers.append(dict(zip(variables, rooms)))
assert csp_answers == oracle_answers
print("Nghiệm CSP:", csp_answers)
print("Khớp vét cạn:", csp_answers == oracle_answers)

# Bước 7
worlds = list(product([False, True], repeat=3))
models = [(P, Q, R) for P, Q, R in worlds if P and (P != Q) and (Q != R)]
models_without_P = [(P, Q, R) for P, Q, R in worlds if (P != Q) and (Q != R)]
assert models                  # kiểm KB có nghiệm trước khi diễn giải
entails_R = all(R for P, Q, R in models)
counterexamples = [world for world in models_without_P if not world[2]]
print("Models của KB:", models)
print("KB suy ra R:", entails_R)
print("Bỏ P, phản ví dụ cho R:", counterexamples)
assert entails_R and counterexamples
