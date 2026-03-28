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

        # simulate realistic order load (peak vs normal)
        if random.random() < 0.5:
            self.orders = random.randint(3, 7)  # peak hours
        else:
            self.orders = random.randint(1, 4)  # normal hours

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

        # Actions:
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
                reward += 18  # efficient batching
            else:
                reward -= 3

        elif action == 3:
            if self.pending_orders > 0:
                self.pending_orders -= 1
                self.waste += 1
                reward -= 5

        # time progresses
        self.time += 1
        reward -= 1  # time penalty

        # delay penalty (if too many pending after time passes)
        if self.pending_orders > 0 and self.time > 5:
            reward -= 2

        # completion bonus
        if self.pending_orders == 0:
            reward += 20

        # done condition
        if self.time >= self.max_time or self.pending_orders == 0:
            done = True

        return self.state(), reward, done


# =============================
# Smart Agent (Greedy)
# =============================

class GreedyAgent:
    def act(self, state):
        if state["pending_orders"] >= 2:
            return 2  # batch prepare
        elif state["pending_orders"] == 1:
            return 1  # prepare single
        else:
            return 0  # do nothing


# =============================
# Run Simulation
# =============================

def run_episode():
    env = CanteenEnv()
    agent = GreedyAgent()

    state = env.reset()
    total_reward = 0

    print("\n--- New Episode ---")

    while True:
        action = agent.act(state)
        state, reward, done = env.step(action)

        print(f"Time: {state['time']} | Pending: {state['pending_orders']} | Completed: {state['completed_orders']} | Reward: {reward}")

        total_reward += reward

        if done:
            break

    print(f"Final Score: {total_reward}")
    return total_reward


# =============================
# Main Execution
# =============================

if __name__ == "__main__":
    episodes = 5

    for i in range(episodes):
        print(f"\n===== Episode {i+1} =====")
        run_episode()


# =============================
# Tasks Definition
# =============================

"""
EASY:
- Handle single order efficiently

MEDIUM:
- Manage multiple orders with batching

HARD:
- Minimize waste + maximize profit + reduce delay
"""
