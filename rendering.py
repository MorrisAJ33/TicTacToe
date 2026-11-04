from sprites import grid, v, h, x, o, b
import time

class Game:
    def __init__(self, agent_1=None, agent_2=None, _render=True):
        self.game = self._start_game()
        self.player = 'X'
        self.plays = {'X': x, 'O': o}
        self.players = {'X':'agent' if agent_1 else 'human', 'O':'agent' if agent_2 else 'human'}
        self.numeric_board = [0]*9
        self.numeric_play = {'X':1, 'O':2}
        self.winner = False
        self._horizontal = [(1,2,3),(4,5,6),(7,8,9)]
        self._vertical = [(1,4,7),(2,5,8),(3,6,9)]
        self._diagonal = [(1,5,9),(3,5,7)]
        self.actions = 0
        self.agents = {'X':agent_1, 'O':agent_2}
        self.render = True
        if (agent_1 and agent_2) and not _render:
            self.render = False

        self.reward=None
        self.winner=None

    def reset(self):
        self.game = self._start_game
        self.reward = None
        self.winner = None

    def _next_turn(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
    
    def _start_game(self):
        for i, section in enumerate(grid.keys()):
            grid[section] = b[:-2] + f"{i + 1}\n"

        return grid

    def _draw_game(self):
        board = ""
        for g_L, g_M, g_R in self._horizontal:
            for line in zip(self.game[g_L].split('\n'), v.split('\n'), self.game[g_M].split('\n'),
                            v.split('\n'), self.game[g_R].split('\n')):
                board += f"{''.join(line)}\n"

            if g_L != 7:
                board = board[:-1] + h

        print(board[:-1])

    def __resolve(self, winning_sequence):
        for position in self.game.keys():
            if position not in winning_sequence:
                self.game[position] = b
        self.winner = True

    def __check_game(self, positions):
        one, two, three = positions
        if self.game[one] == self.game[two] == self.game[three]:
            self.__resolve([one, two, three])

    def _board_status(self):
        for positions in [*self._horizontal, *self._vertical, *self._diagonal]:
            self.__check_game(positions)
            if self.winner:
                if self.render:
                    self._draw_game()
                return
                
    def play(self):
        if (self.render and self.players[self.player] != "agent") or (self.players['X'] =="agent" and self.players['O']
            == "agent" and self.player == 'X' and self.render):
            self._draw_game()
        play = " "
        if self.actions == 9:
            if self.render:
                print(rf"""
 ___    ___         
|   \  |   \     /\   \            / ||
|    | |   |    /  \   \    /\    /  || 
|    | |---\   /————\   \  /  \  /   ||
|———/  |    \ /      \   \/    \/    .. 

""")
            self.reward = 0
            self.winner = self.player
            return

        msg = f"Player {self.player} Select Location as Number: "
        valid_plays = [f"{i + 1}" for i, p in enumerate(self.numeric_board) if p == 0]
        while play not in valid_plays:
            if self.players[self.player] == "agent":
                action = self.agents[self.player].step(self.numeric_board)
                play = str(action + 1)
                if play not in valid_plays:
                    raise ValueError(f"Agent Play: {play} not in valid location {', '.join(valid_plays)}")

                if self.render:
                    time.sleep(1.5)
            else:
                play = input(msg)
                msg = msg.replace(': ', " Valid Grid #'s " + ', '.join(valid_plays) + '(enter):')

        self.game[int(play)] = self.plays[self.player]
        self.numeric_board[int(play)-1] = self.numeric_play[self.player]

        self._board_status()

        if self.winner:
            if self.render:
                print(f"Winner {self.player}'s")
            self.reward = 1
            self.winner = self.player
            return

        self._next_turn()
        self.actions += 1
        self.play()
