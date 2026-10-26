from sprites import grid, v, h, x, o, b

class Game:
    def __init__(self):
        self.game = self._start_game()
        self.player = 'X'
        self.plays = {'X': x, 'O': o}
        self.winner = False
        self._horizontal = [(1,2,3),(4,5,6),(7,8,9)]
        self._vertical = [(1,4,7),(2,5,8),(3,6,9)]
        self._diagonal = [(1,5,9),(3,5,7)]
        self.actions = 0

    def reset(self):
        self.game = self._start_game

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
        for one, two, three in positions:
            if self.game[one] == self.game[two] == self.game[three]:
                self.__resolve([one, two, three])

    def _board_status(self):
        for positions in [self._horizontal, self._vertical, self._diagonal]:
            self.__check_game(positions)
            if self.winner:
                self._draw_game()
                return
                
    def play(self):
        self._draw_game()
        play = " "
        if self.actions == 9:
            print(rf"""
 ___    ___         
|   \  |   \     /\   \            / ||
|    | |   |    /  \   \    /\    /  || 
|    | |---\   /————\   \  /  \  /   ||
|———/  |    \ /      \   \/    \/    .. 

""")
            return

        msg = f"Player {self.player} Select Location as Number: "
        valid_plays = ["not parsed"]
        while play not in valid_plays:
            play = input(msg)
            valid_plays = [grid[section][-2] for section in grid.keys() if grid[section][-2].isdigit()]
            msg = msg.replace(': ', " Valid Grid #'s " + ', '.join(valid_plays) + '(enter):')

        self.game[int(play)] = self.plays[self.player]

        self._board_status()

        if self.winner:
            print(f"Winner {self.player}'s")
            return

        self._next_turn()
        self.actions += 1
        self.play()
