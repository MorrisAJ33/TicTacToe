from rendering import Game
from ai_gym_env import TicTacToeEnv, np, _load_model
import pickle
import argparse

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--agent",
        help="Use Text with - O for Computer to Play O's - X for Computer to Play X's or both for both simulated players",
        required=False,
        type=str
    )
    parser.add_argument(
        "-d",
        "--difficulty",
        help="Number: 0 to 5",
        required=False,
        type=int
    )

    return parser.parse_args()

def _run(agent_1, agent_2):
    jam = True
    total_wins = {'X':0, 'O':0, 'DRAW':0}
    while jam:
        current_game = Game(agent_1=agent_1, agent_2=agent_2)
        current_game.play()
        if current_game.reward == 0:
            total_wins['DRAW'] += 1
        else:
            total_wins[current_game.winner] += 1

        response = input('Play another Game (Y/N): ')
        response = response.upper()[0] if response else 'N'
        if response == 'Y':
            jam = True
            print("Let's Start Again!")
            current_game.reset()
        else:
            jam = False
            print("No Fun Quitters")
            print(f"Games Won: {' | '.join([k+' = '+str(v) for k,v in total_wins.items() if v > 0])}")


def main(agents, difficulty):
    agent_1 = None
    agent_2 = None
    #DIFFICULTY = {0:"Basic", 1:"Beginner", 2:"Intermediate", 3: "Advanced", 4:"Hard", 5:"Hardest"}
    DIFFICULTY = {1: "Beginner", 2: "Advanced", 3: "Hardest"}
    suffix = 2
    if difficulty:
        suffix = difficulty
    if "X" in agents:
        agent_table = _load_model(f"X_model_{suffix}.pkl")
        agent_1 = TicTacToeEnv(model=agent_table)
    if "O" in agents:
        agent_table = _load_model(f"O_model_{suffix}.pkl")
        agent_2 = TicTacToeEnv(model=agent_table)

    if agents:
        msg = f"Input: {agents}\n"
        if agent_1:
            msg += "\tSimulating 'X' Player\n"
        if agent_2:
            msg += "\tSimulating 'O' Player\n"

        if not agent_1 and not agent_2:
            msg += "Must include 'X', 'O', or both to simulate player with agent\n"
        else:
            msg += f"Agent Difficulty at {DIFFICULTY[suffix]}"
        print(msg)

    _run(agent_1, agent_2)

if __name__ == "__main__":
    args = _parse_args()
    if not args.agent:
        pass
    elif not args.difficulty:
        print(f"Default Difficulty = 1")
    elif 3 < args.difficulty < 1:
        print(f"Invalid Difficulty: {args.difficulty} - setting defaulting to 2")
        args.difficulty = 3

    main(args.agent, args.difficulty)