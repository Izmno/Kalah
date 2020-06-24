from kalah import Kalah
import signal

class KalahUi:
    def __init__(self):
        self.game = Kalah(5, 5)
        self.maxSeeds = 50
        self.maxDigits = 2

        self.padding = ' ' * 12
        self.player1string = '  Player 1  '
        self.player2string = '  Player 2  '

        self.canContinue = True

    def interrupt(self):
        self.canContinue = False

    def formatFirstPlayer(self, player):
        invert = player % 2 == 1
        padding = ' ' * 12
        playerstring = f'  Player {player + 1}  '

        playerSeeds = [padding]
        playerSeeds += [f'[{str(seeds).rjust(self.maxDigits)}]  ' for seeds in self.game.getPlayerSlice(player, includeStore = False)]
        playerSeeds += [playerstring]
        
        playerHouses = [padding]
        playerHouses += [f' {str(house).rjust(self.maxDigits)}   ' for house in range(1, self.game._houses + 1)] 
        playerHouses += [padding]

        return [''.join(playerSeeds[::-1 if invert else 1]), ''.join(playerHouses[::-1 if invert else 1])][::-1 if invert else 1]

    def formatStores(self):
        lead = ' ' * 4
        trail = ' ' * (12 - 6 - self.maxDigits)
        store1 = self.game.board[self.game.storeIndex(0)]
        store2 = self.game.board[self.game.storeIndex(1)]
        store1str = f'[{str(store1).rjust(self.maxDigits)}]'
        store2str = f'[{str(store2).rjust(self.maxDigits)}]'
        spaces = self.game._houses * (4 + self.maxDigits) * ' '
        return lead + store2str + trail + spaces + trail + store1str + lead

    def formatState(self):
        return f'\n> Next player: {self.game.nextPlayer + 1}. Select your move (1-{self.game._houses})\n'

    def formatField(self):
        return '\n'.join(self.formatFirstPlayer(1) + [self.formatStores()] + self.formatFirstPlayer(0))

    def run(self):
        while not self.game.gameEnded and self.canContinue:
            print(self.formatField())
            print(self.formatState())

            move = None
            while move is None:
                try:
                    inp = input()
                    if inp == 'q':
                        return
                    
                    move = (int(inp) - 1 ) % self.game._houses
                    print(f"> Moving house {move + 1}")
                except:
                    print("> Not a valid move. Try again\n")
            
            self.game.move(move)

        print(self.formatField())
        print(self.formatState())
        
        winner = self.game.winningPlayer()
        if winner is not None:
            print(f"> Game has ended. Player {self.game.winningPlayer() + 1} won!")
        else:
            print("> Game has ended. Game ended in a tie!")

        
        

if __name__ == '__main__':
    g = KalahUi()
    signal.signal(signal.SIGINT, g.interrupt)

    g.run()
        