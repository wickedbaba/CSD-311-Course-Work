from game import Game
from computer import Computer
from move import Move
from game import bcolors

checkers = Game()
checkers.newGame()

gameOver = False

aiPlayer = Computer(1)
choice = 0
numMoves = 0

while (choice < 1 or choice > 2):
    print("\n\nChoose the Game Algorithm:-")
    print(bcolors.GREEN + "1 for Random" + bcolors.RESET)
    print(bcolors.GREEN + "2 for Minmax" + bcolors.RESET)
    choice = int(input())
    if(choice != 1 and choice != 2):
        print("Type valid choice only!")


while not gameOver or numMoves <= 50:
    moveNumber = -1
    if checkers.currentPlayer == 1:
        legalMoves = checkers.getLegalMoves(checkers.board)
        if len(legalMoves) == 0:
            gameOver = True
            print("Human Wins!")
            continue

        print("\nComputer's Turn: ")

        move = None
        if(choice == 1):
            move = aiPlayer.randomMove(checkers)
        else:
            move = aiPlayer.minMaxSearch(checkers)

        checkers.applyMove(move, checkers.board)
        numMoves += 1
        print("Computer Chose: ", end='')
        checkers.printMove(move)

        checkers.showBoard()

    elif checkers.currentPlayer == 2:
        legalMoves = checkers.getLegalMoves(checkers.board)
        if len(legalMoves) == 0:
            gameOver = True
            print("\nComputer Wins!")
            continue

        print("\nHuman's Turn: ")
        checkers.printListMoves(legalMoves)

        while (moveNumber < 0 or moveNumber >= len(legalMoves)):
            print("Choose a move number (e.g. type 0 and hit enter): ")
            try:
                moveNumber = int(input())
            except:
                print("Type valid move numbers only!")

        checkers.applyMove(legalMoves[moveNumber], checkers.board)
        numMoves += 1
        print("Human Chose: ")
        checkers.printMove(legalMoves[moveNumber])
        checkers.showBoard()
