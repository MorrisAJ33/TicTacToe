from rendering import Game

def main():
    jam = True
    while jam:
        current_game = Game()
        current_game.play()
        response = input('Play another Game (Y/N): ').upper()[0]
        if response == 'Y':
            jam = True
            print("Let's Start Again!")
            current_game.reset()
        else:
            jam = False
            print("No Fun Quitters")

if __name__ == "__main__":
    main()