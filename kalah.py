class Kalah:
    def __init__(self, houses, seeds):
        self._houses = houses

        # half the size of the board, i.e. number of houses and the store
        # for each player
        self._halfsize = houses + 1

        # full size of the board
        self._fullsize = 2 * self._halfsize

        # board: array of length fullsize
        #   positions 0 mod halfsize are stores -> initialized to 0
        #   other positions are houses -> initialized to number of starting seeds
        self.board = [ 0 if self.isStore(index) else seeds for index in range(self._fullsize) ]

        # nextPlayer: integer mod 2 representing player to make next move
        self.nextPlayer = 0

        # gameEnded: boolean indicating whether the game has ended
        self.gameEnded = False

    def startIndex(self, player):
        return (player % 2) * self._halfsize

    def storeIndex(self, player):
        return (((player + 1) % 2) * self._halfsize - 1 ) % self._fullsize

    def houseIndex(self, house, player):
        return (player % 2) * self._halfsize + (house % self._houses)

    def isStore(self, index):
        return index % self._halfsize == self._halfsize - 1

    def components(self, index):
        house = index % (self._halfsize) 
        player = index // (self._halfsize) % 2
        seeds = self.board[index % (self._fullsize)]
        isStore = self.isStore(index)

        return (house, player, seeds, isStore)

    def getPlayerSlice(self, player, includeStore = False):
        endIndex = self.storeIndex(player) + 1 if includeStore else self.storeIndex(player)
        return self.board[self.houseIndex(0, player): endIndex]

    def seedsInHouses(self, player, includeStore = False):
        return sum(self.getPlayerSlice(player, includeStore))

    def gameShouldEnd(self):
        return self.seedsInHouses(0) == 0 or self.seedsInHouses(1) == 0

    def empty(self, house, player):
        seeds = self.board[self.houseIndex(house, player)]
        self.board[self.houseIndex(house, player)] = 0
        return seeds        

    def moveToStore(self, house, player, includeOpponent = True ):
        seeds = self.empty(house, player)
        if includeOpponent:
            seeds += self.empty(- house - 1, player + 1)
        self.board[self.storeIndex(player)] += seeds

    def finish(self):
        self.board = [self.seedsInHouses(index // self._halfsize, True) if self.isStore(index) else 0 for index in range(self._fullsize)]
        self.gameEnded = True

    def winningPlayer(self):
        p0 = self.board[self.storeIndex(0)]
        p1 = self.board[self.storeIndex(1)]
        if p0 > p1:
            return 0
        if p1 > p0:
            return 1
        return None
        

    def move(self, house):
        player = self.nextPlayer
        seeds = self.empty(house, player)

        if house == 0:
            print(seeds)
        
        if seeds == 0: 
            # if the selected house was empty
            # end the move without changing player
            return False
        
        index = self.houseIndex(house, player)
        while seeds > 0:
            # loop around the board while we have seeds left
            index += 1
            if index != self.storeIndex(player + 1):
                # Unless index points to the store of the opposing player
                # drop a seed
                seeds -= 1
                self.board[index % self._fullsize] += 1

        # get info on ending index
        house, iplayer, seeds, isStore = self.components(index)
        
        if iplayer == player and not isStore and seeds == 1:
            # if move ends on an empty house of the current player
            # move seeds to store
            self.moveToStore(house, player)

        if not ( iplayer == player and isStore ):
            # if move does not end on store of current player
            # change the current player
            self.nextPlayer = (player + 1) % 2
        
        if self.gameShouldEnd():
            # if any player has no seeds in houses
            # end the game
            self.finish()

        return True