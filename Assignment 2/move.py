class Move:
    def __init__(self, *args):   # constructor to initialize move list with default values
        if len(args) == 1:
            self.initialRow = args[0].initialRow
            self.initialCol = args[0].initialCol
            self.startRow = args[0].startRow
            self.startCol = args[0].startCol
            self.endRow = args[0].endRow
            self.endCol = args[0].endCol
            self.state = args[0].state
            self.listCaptureRow = args[0].listCaptureRow
            self.listCaptureCol = args[0].listCaptureCol
            self.listVisitedRow = args[0].listVisitedRow
            self.listVisitedCol = args[0].listVisitedCol
            self.capturedSquares = args[0].capturedSquares
        else:
            self.initialRow = 0
            self.initialCol = 0
            self.startRow = args[0]
            self.startCol = args[1]
            self.endRow = args[2]
            self.endCol = args[3]
            self.state = args[4]
            self.listCaptureRow = []
            self.listCaptureCol = []
            self.listVisitedRow = []
            self.listVisitedCol = []
            self.capturedSquares = []
