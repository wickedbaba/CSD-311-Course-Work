from move import Move
from game import Game
import random
import sys
from copy import deepcopy


class Computer:

    def __init__(self, maximizingPlayer):
        self.maximizingPlayer = maximizingPlayer
        self.maxDepth = 0

    def randomMove(self, game: Game) -> Move:   # Algorithm for Random Moves
        legalMovesList = game.getLegalMoves(game.board)
        return random.choice(legalMovesList)

    def minMaxSearch(self, game: Game) -> Move:  # Algorithm for Minmax Search
        bestMoveVal = 0
        depthReached = 0
        bestMove = None
        legalMovesList = game.getLegalMoves(game.board)

        if(len(legalMovesList) == 1):
            print("Searched to depth 0")
            return legalMovesList[0]

        for maxDepth in range(10):
            listBestMovesCurrentDepth = []
            bestVal = -2**31
            for move in legalMovesList:
                copyGame = deepcopy(game)
                copyGame.applyMove(move, copyGame.board)
                min = self.minVal(copyGame, -2**31, 2**31, 0)
                if(min == bestVal):
                    listBestMovesCurrentDepth.append(move)
                if(min > bestVal):
                    listBestMovesCurrentDepth.clear()
                    listBestMovesCurrentDepth.append(move)
                    bestVal = min
                if(bestVal == 2**31):
                    break
            bestMove = random.choice(listBestMovesCurrentDepth)
            depthReached = maxDepth
            bestMoveVal = bestVal

            if(bestMoveVal == 2**31):
                break

        return bestMove

    # checks whether program has reached max depth or leaf node
    def cutoffTest(self, numMoves: int, depth: int) -> bool:
        if (numMoves == 0 or depth == self.maxDepth):
            return True
        else:
            return False

    # returns number of neighbours for a particular piece
    def numDefendingNeighbors(self, row: int, col: int, state: list) -> int:
        defense = 0

        if(state[row][col] == 1):
            if(row + 1 < len(state) and col + 1 < len(state[0])):
                if((state[row + 1][col + 1] & 1) == 1):
                    defense += 1

            if(row + 1 < len(state) and col - 1 >= 0):
                if((state[row + 1][col - 1] & 1) == 1):
                    defense += 1

        elif(state[row][col] == 2):
            if(row - 1 >= 0 and col + 1 < len(state[0])):
                if((state[row - 1][col + 1] & 1) == 0):
                    defense += 1
            if(row - 1 >= 0 and col - 1 >= 0):
                if((state[row - 1][col - 1] & 1) == 0):
                    defense += 1

        elif(state[row][col] == 3):
            if(row + 1 < len(state) and col + 1 < len(state[0])):
                if((state[row + 1][col + 1] & 1) == 1):
                    defense += 1

            if(row + 1 < len(state) and col - 1 >= 0):
                if((state[row + 1][col - 1] & 1) == 1):
                    defense += 1

            if(row - 1 >= 0 and col + 1 < len(state[0])):
                if((state[row - 1][col + 1] & 1) == 1):
                    defense += 1

            if(row - 1 >= 0 and col - 1 >= 0):
                if((state[row - 1][col - 1] & 1) == 1):
                    defense += 1

        elif(state[row][col] == 4):
            if(row + 1 < len(state) and col + 1 < len(state[0])):
                if((state[row + 1][col + 1] & 1) == 0):
                    defense += 1

            if(row + 1 < len(state) and col - 1 >= 0):
                if((state[row + 1][col - 1] & 1) == 0):
                    defense += 1

            if (row - 1 >= 0 and col + 1 < len(state[0])):
                if ((state[row - 1][col + 1] & 1) == 0):
                    defense += 1

            if (row - 1 >= 0 and col - 1 >= 0):
                if ((state[row - 1][col - 1] & 1) == 0):
                    defense += 1
        return defense

    # to account for number of pieces left , king's pieces and game status
    def heuristic(self, game: Game) -> int:
        boardVal = 0
        for i in range(8):
            for j in range(8):
                if self.maximizingPlayer == 1:
                    if game.board[i][j] == 1:
                        boardVal += 3 + \
                            (i * 0.5) + self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal += 1
                        if i == 0:
                            boardVal += 2
                    elif game.board[i][j] == 2:
                        boardVal -= 3 + \
                            ((7 - i) * 0.5) + \
                            self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal -= 1
                        if i == 7:
                            boardVal -= 2
                    elif game.board[i][j] == 3:
                        boardVal += 5 + \
                            self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal += 1
                        if i == 0:
                            boardVal += 2
                    elif game.board[i][j] == 4:
                        boardVal -= 5 + \
                            self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal -= 1
                        if i == 7:
                            boardVal -= 2
                else:
                    if game.board[i][j] == 1:
                        boardVal -= 3 + \
                            (i * 0.5) + self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal -= 1
                        if i == 0:
                            boardVal -= 2
                    elif game.board[i][j] == 2:
                        boardVal += 3 + \
                            ((7 - i) * 0.5) + \
                            self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal += 1
                        if i == 7:
                            boardVal += 2
                    elif game.board[i][j] == 3:
                        boardVal += 5 + \
                            self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal -= 1
                        if i == 0:
                            boardVal -= 2
                    elif game.board[i][j] == 4:
                        boardVal -= 5 + \
                            self.numDefendingNeighbors(i, j, game.board)
                        if j == 0 or j == 8:
                            boardVal += 1
                        if i == 7:
                            boardVal += 2
        return boardVal

    def minVal(self, game: Game, alpha: int, beta: int, depth: int) -> int:
        listLegalMoves = game.getLegalMoves(game.board)

        if (self.cutoffTest(len(listLegalMoves), depth)):
            return self.heuristic(game)
        v = 2**31

        for i in range(listLegalMoves):
            copyGame = self.Game(game)
            copyGame.applyMove(self.move, copyGame.board)
            v = min(v, self.maxVal(copyGame, alpha, beta, depth + 1))
            if (v <= alpha):
                return v

            beta = min(beta, v)
            return v

    def maxVal(self, game: Game, alpha: int, beta: int, depth: int) -> int:
        listLegalMoves = game.getLegalMoves(game.board)

        if (self.cutoffTest(len(listLegalMoves), depth)):
            return self.heuristic(game)

        v = -2**31

        for i in range(listLegalMoves):
            copyGame = self.Game(game)
            copyGame.applyMove(self.move, copyGame.board)
            v = max(v, self.maxVal(copyGame, alpha, beta, depth + 1))
            if (v >= beta):
                return v

            alpha = min(alpha, v)
        return v
