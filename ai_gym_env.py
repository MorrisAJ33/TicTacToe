import gymnasium as gym
import numpy as np
from rendering import Game
import pickle
from os.path import exists

class TicTacToeEnv(gym.Env):
    def __init__(self, model=None):
        self.action_space = gym.spaces.Discrete(9)
        self.observation_space = gym.spaces.Box(low=0, high=2, shape=(9,), dtype=np.int8)
        self.q_table = np.zeros((3 ** 9, 9)) if model is None else model
        self.epsilon = 0.2
        self.alpha = 0.1
        self.gamma = 0.95
        self.previous_state=None
        self.previous_action=None
        self.train= True if model is None else False

    def reset(self):
        self.previous_state = None
        self.previous_action = None

    def final_reward(self, reward_):
        self.q_table[self.previous_state, self.previous_action] += (
                self.alpha * (reward_ - self.q_table[self.previous_state, self.previous_action]))

    @staticmethod
    def _board_to_state(board):  # board: array of 9 values in {0,1,2}
        return int(sum(v * 3 ** i for i, v in enumerate(board)))

    def _action(self, state, board):
        legal = [i for i in range(9) if board[i] == 0]
        if np.random.rand() < self.epsilon and self.train:
            return np.random.choice(legal)

        q = self.q_table[state].copy()
        mask = np.full(9, -np.inf)
        mask[legal] = q[legal]
        return int(np.argmax(mask))

    def step(self, board):
        state = self._board_to_state(board)
        action = self._action(state, board)
        if self.train:
            if self.previous_state:
                self.q_table[state, action] += (
                self.alpha * (self.gamma * np.max(self.q_table[self.previous_state]) - self.q_table[state, action]))
            else:
                if action in [1,3,5,7]:
                    self.q_table[state, action] += (self.alpha * (-1))
                elif action == 5 and state == 3:
                    self.q_table[state, action] += (self.alpha * 1)
            self.previous_state = state
            self.previous_action = action

        return action

def _load_model(file):
    if not exists(file):
        raise FileNotFoundError(f"No Model created for input: {file.split('.')[0]}")
    with open(file, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    model_suffix = 2
    train_range = 1_000_000
    use_model=True
    if use_model:
        ag1 = _load_model(f"X_model_{model_suffix}.pkl")
        ag2 = _load_model(f"O_model_{model_suffix}.pkl")
    else:
        ag1=None
        ag2=None

    agent_1 = TicTacToeEnv(ag1)
    agent_2 = TicTacToeEnv(ag2)
    """if use_model:
        e=.2
        agent_1.train=True
        agent_1.epsilon = e
        agent_2.train=True
        agent_2.epsilon = e"""

    agents = {'X':agent_1, 'O':agent_2}
    opposites = {'X':'O', 'O':'X'}
    track_wins = {'X':0, 'O':0, 'DRAW': 0}
    for episode in range(train_range):
        agent_1.reset()
        agent_2.reset()
        game = Game(agent_1=agent_1, agent_2=agent_2, _render=False)
        game.play()
        reward = game.reward
        player = game.winner

        agents[player].final_reward(reward)
        agents[opposites[player]].final_reward(reward*-1)
        if reward == 0:
            track_wins['DRAW'] += 1
        else:
            track_wins[player] += 1

    for agent in ['X', 'O']:
        with open(f"{agent}_model_{model_suffix}.pkl", "wb") as f:
            pickle.dump(agents[agent].q_table, f)

    print(f"Wins: {track_wins}")
