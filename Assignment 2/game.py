from move import Move
from copy import deepcopy


class bcolors:
    WHITE_BACKGROUND = '\u001B[47m'
    CYAN = '\u001B[96m'
    RESET = '\u001B[0m'
    RED = '\u001B[91m'
    GREEN = '\u001b[32;1m'
    BACK_RED = '\u001b[41m'
    YELLOW = '\u001b[33;1m'
    KING = '\u039B'
    BOLD = '\033[1m'
    YELLOW_DOT = '\U0001F7E1'
    BLUE_DOT = '\U0001F535'


class Game:
    def __init__(self, *args):
        if len(args) == 0:
            self.board = []
            self.currentPlayer = 1

            for i in range(8):
                temp = []
                for j in range(8):
                    temp.append(0)
                self.board.append(temp)
        else:
            self.board = args[0].board
            self.currentPlayer = args[0].currentPlayer

    def newGame(self):
        # null places = -1
        # empty place = 0
        # player1 (normal) = 1
        # player2 (normal) = 2
        # player1 (king) = 3
        # player2 (king) = 4
        for i in range(3):
            for j in range(0, 8, 2):
                if (i & 1) == 1:
                    self.board[i][j+1] = -1
                    self.board[i][j] = 1
                else:
                    self.board[i][j] = -1
                    self.board[i][j+1] = 1

        for i in range(3, 5):
            for j in range(0, 8, 2):
                if(i & 1) == 1:
                    self.board[i][j+1] = -1
                    self.board[i][j] = 0
                else:
                    self.board[i][j] = -1
                    self.board[i][j+1] = 0

        for i in range(5, 8):
            for j in range(0, 8, 2):
                if(i & 1) == 1:
                    self.board[i][j+1] = -1
                    self.board[i][j] = 2
                else:
                    self.board[i][j] = -1
                    self.board[i][j+1] = 2

    def showBoard(self):                              # GUI Display of Checker Board
        print("      0      1      2      3      4      5      6      7   ")
        for i in range(8):
            print("   ", end='')
            if((i & 1) == 0):
                for j in range(4):
                    print(bcolors.WHITE_BACKGROUND +
                          "       " + bcolors.BACK_RED + "       "+bcolors.RESET, end='')
                print()

                print(f' {i} ', end='')

                for j in range(8):
                    self.printPieces(self.board[i][j])

                print()
                print("   ", end='')

                for j in range(4):
                    print(bcolors.WHITE_BACKGROUND +
                          "       " + bcolors.BACK_RED + "       "+bcolors.RESET, end='')

            else:
                for j in range(4):
                    print(bcolors.BACK_RED+"       " + bcolors.WHITE_BACKGROUND +
                          "       " + bcolors.RESET, end='')

                print()
                print(f' {i} ', end='')

                for j in range(8):
                    self.printPieces(self.board[i][j])

                print()
                print("   ", end='')

                for j in range(4):
                    print(bcolors.BACK_RED+"       " + bcolors.WHITE_BACKGROUND +
                          "       " + bcolors.RESET, end='')

            print()

    # Helper function to print correct pieces: 1 for AI piece, 2 for User piece, 3 for AI's king, 4 for User's king
    def printPieces(self, val: int):
        if(val == -1):
            print(bcolors.WHITE_BACKGROUND +
                  "       " + bcolors.RESET, end='')
        elif(val == 0):
            print(bcolors.BACK_RED+"       "+bcolors.RESET, end='')
        elif(val == 1):
            print(bcolors.BACK_RED+bcolors.YELLOW +
                  "   ▼   " + bcolors.RESET, end='')
        elif(val == 2):
            print(bcolors.BACK_RED+bcolors.CYAN +
                  "   ▲   " + bcolors.RESET, end='')
        elif(val == 3):
            print(bcolors.BACK_RED+bcolors.YELLOW +
                  "   ⨈   " + bcolors.RESET, end='')
        elif(val == 4):
            print(bcolors.BACK_RED+bcolors.CYAN +
                  "   ⨇   " + bcolors.RESET, end='')

    # Updates the list of all possible valid moves after each turn
    def getLegalMoves(self, state: list) -> list:
        slideMoves = []
        jumpMoves = []
        for i in range(8):
            for j in range(8):
                if(self.currentPlayer == 1):
                    if(self.board[i][j] == 1 or self.board[i][j] == 3):
                        self.getCaptureMoves(jumpMoves, None,
                                             self.board[i][j], i, j, state)
                        if len(jumpMoves) == 0:
                            self.getNormalMove(
                                slideMoves, self.board[i][j], i, j, self.board)
                else:
                    if(self.board[i][j] == 2 or self.board[i][j] == 4):
                        self.getCaptureMoves(jumpMoves, None,
                                             self.board[i][j], i, j, state)
                        if len(jumpMoves) == 0:
                            self.getNormalMove(
                                slideMoves, self.board[i][j], i, j, self.board)
        if(len(jumpMoves) == 0):
            return slideMoves
        return jumpMoves

    # updates list of sliding moves if capture not possible
    def getNormalMove(self, moves: list, pieceType: int, startRow: int, startCol: int, state: list):
        endRow = []
        endCol = []
        if(pieceType == 1):
            endRow.append(startRow + 1)
            endRow.append(startRow + 1)
            endCol.append(startCol + 1)
            endCol.append(startCol - 1)
        elif(pieceType == 2):
            endRow.append(startRow - 1)
            endRow.append(startRow - 1)
            endCol.append(startCol + 1)
            endCol.append(startCol - 1)
        elif(pieceType == 3 or pieceType == 4):
            endRow.append(startRow + 1)
            endRow.append(startRow + 1)
            endRow.append(startRow - 1)
            endRow.append(startRow - 1)
            endCol.append(startCol + 1)
            endCol.append(startCol - 1)
            endCol.append(startCol + 1)
            endCol.append(startCol - 1)

        for i in range(len(endRow)):
            if(endRow[i] < 0 or endRow[i] > 7 or endCol[i] < 0 or endCol[i] > 7):
                continue
            if (state[endRow[i]][endCol[i]] != 0):
                continue
            moves.append(Move(startRow, startCol, endRow[i], endCol[i], state))

    # updates list of capturing moves
    def getCaptureMoves(self, moves: list, move: Move, pieceType: int, startRow: int, startCol: int, state: list):
        endRow = []
        endCol = []
        captureRow = []
        captureCol = []

        if(pieceType == 1):
            endRow.append(startRow + 2)
            endRow.append(startRow + 2)
            endCol.append(startCol - 2)
            endCol.append(startCol + 2)
            captureRow.append(startRow + 1)
            captureRow.append(startRow + 1)
            captureCol.append(startCol - 1)
            captureCol.append(startCol + 1)
        elif(pieceType == 2):
            endRow.append(startRow - 2)
            endRow.append(startRow - 2)
            endCol.append(startCol - 2)
            endCol.append(startCol + 2)
            captureRow.append(startRow - 1)
            captureRow.append(startRow - 1)
            captureCol.append(startCol - 1)
            captureCol.append(startCol + 1)
        elif(pieceType == 3 or pieceType == 4):
            endRow.append(startRow + 2)
            endRow.append(startRow + 2)
            endRow.append(startRow - 2)
            endRow.append(startRow - 2)
            endCol.append(startCol - 2)
            endCol.append(startCol + 2)
            endCol.append(startCol - 2)
            endCol.append(startCol + 2)
            captureRow.append(startRow + 1)
            captureRow.append(startRow + 1)
            captureRow.append(startRow - 1)
            captureRow.append(startRow - 1)
            captureCol.append(startCol - 1)
            captureCol.append(startCol + 1)
            captureCol.append(startCol - 1)
            captureCol.append(startCol + 1)

        anyValidMoves = False
        whichAreValid = [False for x in endRow]

        for i in range(len(endRow)):
            if(endRow[i] < 0 or endRow[i] > 7 or endCol[i] < 0 or endCol[i] > 7):
                continue
            if(move is not None):
                if(state[endRow[i]][endCol[i]] != 0 and state[endRow[i]][endCol[i]] != state[move.initialRow][move.initialCol]):
                    continue
                if(move.capturedSquares in (captureRow[i], captureCol[i])):
                    continue
            else:
                if(state[endRow[i]][endCol[i]] != 0):
                    continue
            if(self.currentPlayer == 1 and not(state[captureRow[i]][captureCol[i]] == 2 or state[captureRow[i]][captureCol[i]] == 4)):
                continue
            if(self.currentPlayer == 2 and not(state[captureRow[i]][captureCol[i]] == 1 or state[captureRow[i]][captureCol[i]] == 3)):
                continue

            anyValidMoves = True
            whichAreValid[i] = True

        if(move is not None and not(anyValidMoves)):
            moves.append(move)
            return

        if(move is None and anyValidMoves):
            for i in range(len(endRow)):
                if(whichAreValid[i]):
                    newMove = Move(startRow, startCol,
                                   endRow[i], endCol[i], state)
                    newMove.initialRow = startRow
                    newMove.initialCol = startCol
                    newMove.startRow = startRow
                    newMove.startCol = startCol
                    newMove.endRow = endRow[i]
                    newMove.endCol = endCol[i]
                    newMove.listCaptureRow.append(captureRow[i])
                    newMove.listCaptureCol.append(captureCol[i])
                    newMove.listVisitedRow.append(endRow[i])
                    newMove.listVisitedCol.append(endCol[i])
                    newMove.capturedSquares.append(
                        (captureRow[i], captureCol[i]))
                    self.getCaptureMoves(moves, newMove, pieceType,
                                         newMove.endRow, newMove.endCol, state)

        if(move is not None and anyValidMoves):
            for i in range(len(endRow)):
                if(whichAreValid[i]):
                    # newMove = Move(move)
                    # newMove = Move()
                    newMove = deepcopy(move)
                    newMove.startRow = startRow
                    newMove.startCol = startCol
                    newMove.endRow = endRow[i]
                    newMove.endCol = endCol[i]
                    newMove.listCaptureRow.append(captureRow[i])
                    newMove.listCaptureCol.append(captureCol[i])
                    newMove.listVisitedRow.append(endRow[i])
                    newMove.listVisitedCol.append(endCol[i])
                    newMove.capturedSquares.append(
                        (captureRow[i], captureCol[i]))
                    self.getCaptureMoves(moves, newMove, pieceType,
                                         newMove.endRow, newMove.endCol, state)

    # applies the given move and update the game board
    def applyMove(self, move: Move, state: list):
        if len(move.listCaptureRow) == 0:
            state[move.endRow][move.endCol] = state[move.startRow][move.startCol]

            if(state[move.startRow][move.startCol] == 1 and move.endRow == 7):
                state[move.endRow][move.endCol] += 2

            if(state[move.startRow][move.startCol] == 2 and move.endRow == 0):
                state[move.endRow][move.endCol] += 2

            state[move.startRow][move.startCol] = 0

        else:
            for i in range(len(move.listCaptureRow)):
                state[move.listCaptureRow[i]][move.listCaptureCol[i]] = 0

            state[move.endRow][move.endCol] = state[move.initialRow][move.initialCol]

            if(state[move.initialRow][move.initialCol] == 1 and move.endRow == 7):
                state[move.endRow][move.endCol] += 2

            if (state[move.initialRow][move.initialCol] == 2 and move.endRow == 0):
                state[move.endRow][move.endCol] += 2

            state[move.initialRow][move.initialCol] = 0

        if(self.currentPlayer == 1):
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

    def printListMoves(self, moves: Move):
        if len(moves[0].listCaptureRow) == 0:
            for i in range(len(moves)):
                print(
                    f"Move {i} : ({moves[i].startRow}, {moves[i].startCol}) -> ({moves[i].endRow}, {moves[i].endCol})")
        else:
            for i in range(len(moves)):
                print()
                print(
                    f'Move {i} : ({moves[i].initialRow}, {moves[i].initialCol})', end='')
                for j in range(len(moves[i].listVisitedRow)):
                    print(
                        f' -> ({moves[i].listVisitedRow[j]}, {moves[i].listVisitedCol[j]})', end='')
            print()

    def printMove(self, moves: Move):
        if len(moves.listCaptureRow) == 0:
            print(
                f"Move : ({moves.startRow}, {moves.startCol}) -> ({moves.endRow}, {moves.endCol})")
        else:
            print(f'Move : ({moves.initialRow}, {moves.initialCol})', end='')
            for i in range(len(moves.listVisitedRow)):
                print(
                    f' -> ({moves.listVisitedRow[i]}, {moves.listVisitedCol[i]})', end='')
            print()
        print()
