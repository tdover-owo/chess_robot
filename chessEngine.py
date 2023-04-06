""" store all the informison abot the cournt state of a chess game, also choose if the user chose a valide move , move log """

class GameState():
    def __init__(self):
        # bord is 8x8 2d list. every piece have 2 cher first cher is the color and the secand is the Type of a chess piece. the string "--" is empty space
        self.board = [
            ["bR", "bN", "bB" , "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB" , "wQ", "wK", "wB", "wN", "wR"],
            ]
        self.WhiteToMove = True
        self.movelog = []

    def Makemove(self, move):
        self.board[move.startRow][move.startCol] = "--" 
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) #log all the moves in a list
        self.WhiteToMove = not self.WhiteToMove
  
        


class Move():
    
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()} #filp the values of the pygame to be like chess borad
    filesToCols = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,"g": 6,"h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self,startSq,endSq,board) :
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured =board[self.endRow][self.endCol]


    def getChessNotiaon(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    def getRankFile(self,r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    







