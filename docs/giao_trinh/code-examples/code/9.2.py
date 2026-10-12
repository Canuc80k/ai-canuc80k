# -*- coding: utf-8 -*-
# Code mẫu — Tìm kiếm và suy luận

# Ví dụ 1: Đi qua ít cửa nhất trên một bản đồ
from collections import deque

graph = {"S": ["B", "A"], "A": ["G"], "B": ["C"], "C": ["G"], "G": []}
queue, seen = deque([["S"]]), {"S"}
answer = None
while queue:
    path = queue.popleft()
    if path[-1] == "G":
        answer = path
        break
    for following in graph[path[-1]]:
        if following not in seen:
            seen.add(following)
            queue.append(path + [following])

def all_paths(path):
    if path[-1] == "G":
        return [path]
    results = []
    for following in graph[path[-1]]:
        if following not in path:
            results.extend(all_paths(path + [following]))
    return results

oracle = all_paths(["S"])
assert len(answer) - 1 == min(len(path) - 1 for path in oracle) == 2
print("BFS:", answer, "số cửa:", len(answer) - 1)
print("độ dài mọi đường:", sorted(len(path) - 1 for path in oracle))


# Ví dụ 2: Heuristic ước lượng quá tay có thể đưa A* vào đường đắt
import heapq
import math

graph = {"S": [("B", 1), ("A", 2)], "A": [("G", 2)],
         "B": [("G", 9)], "G": []}

def astar(heuristic):
    heap = [(heuristic["S"], 0, "S", ("S",))]
    best = {"S": 0}
    opened = []
    while heap:
        _, cost, node, path = heapq.heappop(heap)
        if cost != best[node]:
            continue
        opened.append(node)
        if node == "G":
            return cost, path, opened
        for following, edge_cost in graph[node]:
            candidate = cost + edge_cost
            if candidate < best.get(following, math.inf):
                best[following] = candidate
                heapq.heappush(heap, (candidate + heuristic[following],
                                     candidate, following, path + (following,)))
    return math.inf, (), opened

def exact_remaining(node, used=()):
    if node == "G":
        return 0
    return min((cost + exact_remaining(following, used + (node,))
                for following, cost in graph[node] if following not in used),
               default=math.inf)

truth = {node: exact_remaining(node) for node in graph}
good = {"S": 4, "A": 2, "B": 9, "G": 0}
bad = {"S": 0, "A": 20, "B": 0, "G": 0}
assert all(0 <= good[node] <= truth[node] for node in graph)
assert all(good[node] <= cost + good[following]
           for node in graph for following, cost in graph[node])
for name, h in [("h=0", dict.fromkeys(graph, 0)), ("lower bound", good), ("phóng đại", bad)]:
    cost, path, opened = astar(h)
    print(name, "giây:", cost, "đường:", path, "mở:", opened)
assert astar(good)[0] == truth["S"] == 4
assert astar(bad)[0] == 10
print("h sai tại:", [node for node in graph if bad[node] > truth[node]])


# Ví dụ 3: Beam rộng hơn cứu được một nhánh khởi đầu yếu
graph = {"S": [("A", 6), ("B", 5)], "A": [("G", 0)],
         "B": [("C", 10)], "C": [("G", 0)], "G": []}

def exhaustive(node="S", path=("S",), score=0):
    if node == "G":
        return [(score, path)]
    results = []
    for following, extra in graph[node]:
        if following not in path:
            results.extend(exhaustive(following, path + (following,), score + extra))
    return results

def beam(width):
    frontier, completed = [(0, ("S",))], []
    kept_by_level = []
    for _ in range(3):
        candidates = []
        for score, path in frontier:
            for following, extra in graph[path[-1]]:
                if following not in path:
                    item = (score + extra, path + (following,))
                    if following == "G":
                        completed.append(item)
                    else:
                        candidates.append(item)
        frontier = sorted(candidates, reverse=True)[:width]
        kept_by_level.append([path[-1] for score, path in frontier])
        if not frontier:
            break
    return max(completed), kept_by_level

optimum = max(exhaustive())
print("vét cạn:", optimum)
for width in [1, 2]:
    result, trace = beam(width)
    print("beam", width, "kết quả:", result, "nhánh giữ:", trace)
    if width == 2:
        assert result == optimum
assert beam(1)[0][0] == 6 and optimum[0] == 15

