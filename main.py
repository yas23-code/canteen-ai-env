# =============================
# AI Canteen Preorder OpenEnv
# =============================

import random

class CanteenEnv:
    def __init__(self):
        self.max_time = 10
        self.reset()

    def reset(self):
        self.time = 0
        self.orders = random.randint(1, 5)
        self.pending_orders = self.orders
        self.completed_orders = 0
        self.waste = 0
        return self.state()

    def state(self):
        return {
            "time": self.time,
            "pending_orders": self.pending_orders,
            "completed_orders": self.completed_orders,
            "waste": self.waste
        }

    def step(self, action):
        reward = 0
        done = False

        # Actions
        # 0 = do nothing
        # 1 = prepare order
        # 2 = batch prepare (2 orders)
        # 3 = reject order

        if action == 1:
            if self.pending_orders > 0:
                self.pending_orders -= 1
                self.completed_orders += 1
                reward += 10
            else:
                reward -= 2

        elif action == 2:
            if self.pending_orders >= 2:
                self.pending_orders -= 2
                self.completed_orders += 2
                reward += 18  # slightly better than 2x single
            else:
                reward -= 3

        elif action == 3:
            if self.pending_orders > 0:
                self.pending_orders -= 1
                self.waste += 1
                reward -= 5

        # time penalty
        self.time += 1
        reward -= 1

        # delay penalty
        if self.pending_orders > 0 and self.time > 5:
            reward -= 2

        # done condition
        if self.time >= self.max_time or self.pending_orders == 0:
            done = True

        return self.state(), reward, done


# =============================
# Simple Agent (Baseline)
# =============================

class RandomAgent:
    def act(self, state):
        return random.choice([0, 1, 2, 3])


# =============================
# Run Simulation
# =============================

def run_episode():
    env = CanteenEnv()
    agent = RandomAgent()

    state = env.reset()
    total_reward = 0

    while True:
        action = agent.act(state)
        state, reward, done = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


if __name__ == "__main__":
    episodes = 10
    for i in range(episodes):
        score = run_episode()
        print(f"Episode {i+1}: Score = {score}")


# =============================
# Tasks Definition (Easy/Medium/Hard)
# =============================

"""
EASY:
- Handle single order efficiently

MEDIUM:
- Manage multiple orders with batching

HARD:
- Minimize waste + maximize profit + reduce delay
"""


# =============================
# Sample openenv.yaml
# =============================

"""
name: canteen-preorder-env
version: 1.0

actions:
  - do_nothing
  - prepare_order
  - batch_prepare
  - reject_order

observations:
  - time
  - pending_orders
  - completed_orders
  - waste

reward:
  prepare_order: +10
  batch_prepare: +18
  reject_order: -5
  delay_penalty: -2
"""


# =============================
# Dockerfile (for deployment)
# =============================

"""
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir
CMD ["python", "main.py"]
"""
