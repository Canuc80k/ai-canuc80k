# -*- coding: utf-8 -*-
# Code mẫu — Reinforcement learning

# Ví dụ 1: Phần thưởng ở bước cuối vẫn được tính vào return
import numpy as np

def step(state, action):
    assert state in [0, 1] and action in [0, 1]
    following = state if action == 0 else state + 1
    terminal = following == 2
    return following, 5.0 if terminal else -1.0, terminal

state, rewards = 0, []
for action in [1, 1]:
    state, reward, terminal = step(state, action)
    rewards.append(reward)
    if terminal:
        break
assert rewards == [-1.0, 5.0] and state == 2
for gamma in [1.0, 0.9, 0.5]:
    value = sum(gamma ** t * reward for t, reward in enumerate(rewards))
    print("gamma:", gamma, "return:", f"{value:.2f}")
print("chờ ở ô 0:", step(0, 0))


# Ví dụ 2: Tính Bellman, và kiểm target có bị lẫn giá trị ô đích không
import numpy as np

gamma = 0.9
def step(state, action):
    assert state < 2
    following = state if action == 0 else state + 1
    terminal = following == 2
    return following, 5.0 if terminal else -1.0, terminal

V = np.zeros(3)
for _ in range(100):
    previous = V.copy()
    for state in [0, 1]:
        options = []
        for action in [0, 1]:
            following, reward, terminal = step(state, action)
            options.append(reward + gamma * (0 if terminal else previous[following]))
        V[state] = max(options)
    if np.max(np.abs(V - previous)) < 1e-12:
        break
assert np.allclose(V, [3.5, 5.0, 0.0])

def target(reward, following_values, terminal):
    return reward if terminal else reward + gamma * np.max(following_values)

print("V*:", V.tolist())
print("target terminal:", target(5.0, np.array([999.0, 999.0]), True))
print("target chưa terminal:", target(-1.0, np.array([2.0, 5.0]), False))
assert target(5.0, np.full(2, 999.0), True) == 5.0


# Ví dụ 3: Agent tự học, rồi được kiểm bằng đường đi
import numpy as np

def step(state, action):
    assert state in [0, 1] and action in [0, 1]
    following = state if action == 0 else state + 1
    terminal = following == 2
    return following, 5.0 if terminal else -1.0, terminal

rng = np.random.default_rng(91)
Q = np.zeros((3, 2))
visits = np.zeros((3, 2), dtype=int)
gamma, alpha, epsilon = 0.9, 0.3, 0.25
for _ in range(400):
    state = 0
    for _ in range(12):
        if rng.random() < epsilon:
            action = int(rng.integers(2))
        else:
            tied = np.flatnonzero(Q[state] == Q[state].max())
            action = int(rng.choice(tied))
        following, reward, terminal = step(state, action)
        target = reward if terminal else reward + gamma * Q[following].max()
        Q[state, action] += alpha * (target - Q[state, action])
        visits[state, action] += 1
        state = following
        if terminal:
            break

saved_Q = Q.copy()
state, path, rewards = 0, [0], []
for _ in range(6):
    state, reward, terminal = step(state, int(np.argmax(Q[state])))
    path.append(state)
    rewards.append(reward)
    if terminal:
        break
observed_return = sum(gamma ** t * reward for t, reward in enumerate(rewards))
assert path == [0, 1, 2] and np.isclose(observed_return, 3.5)
assert np.array_equal(Q, saved_Q) and np.all(Q[2] == 0)
assert np.all(visits[:2] > 0)
print("Q (cột chờ, đi phải):", Q.round(3).tolist())
print("đường greedy:", path, "return:", f"{observed_return:.3f}")
print("mọi cặp không-terminal đã được thử:", bool(np.all(visits[:2] > 0)))

