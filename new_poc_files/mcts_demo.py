import math
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_actions())

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.value / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        tried_actions = [child.state.last_action for child in self.children]
        legal_actions = self.state.get_legal_actions()
        for action in legal_actions:
            if action not in tried_actions:
                next_state = self.state.move(action)
                child_node = Node(next_state, self)
                self.children.append(child_node)
                return child_node

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_terminal():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self.visits += 1
        self.value += result
        if self.parent:
            self.parent.backpropagate(result)

    def rollout_policy(self, possible_moves):
        return random.choice(possible_moves)

class MCTS:
    def __init__(self, root):
        self.root = root

    def best_action(self, simulations_number):
        for _ in range(simulations_number):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.root.best_child(c_param=0.)

    def tree_policy(self):
        current_node = self.root
        while not current_node.state.is_terminal():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

# Dummy game state for testing
class DummyState:
    def __init__(self, moves_left):
        self.moves_left = moves_left
        self.last_action = None

    def get_legal_actions(self):
        return list(range(self.moves_left))

    def move(self, action):
        next_state = DummyState(self.moves_left - 1)
        next_state.last_action = action
        return next_state

    def is_terminal(self):
        return self.moves_left == 0

    def game_result(self):
        return 1 if self.moves_left % 2 == 0 else -1

# Testing the MCTS
if __name__ == '__main__':
    initial_state = DummyState(10)
    root = Node(initial_state)
    mcts = MCTS(root)
    best_node = mcts.best_action(1000)
    print(f'Best action: {best_node.state.last_action}')
    print(f'Best node visits: {best_node.visits}')
    print(f'Best node value: {best_node.value}')
    print(f'Root visits: {root.visits}')
    print(f'Root value: {root.value}')
