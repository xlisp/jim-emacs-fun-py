import unittest
from mcts_demo import MCTS, DummyGame

class TestMCTS(unittest.TestCase):
    def test_mcts_search(self):
        game = DummyGame()
        mcts = MCTS(game, n_iter=100)
        initial_state = game.clone()
        best_state = mcts.search(initial_state)
        self.assertIsNotNone(best_state)

if __name__ == "__main__":
    unittest.main()