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
        self.moveFunciton = {"p" : self.getPwanMoves, "R" : self.getRookMoves , "N" : self.getKnightMoves , "B" : self.getBisopMoves , "Q" : self.getQueenMoves, "K" : self.getKingMoves }
        self.WhiteToMove = True
        self.movelog = []
        self.WhiteKingLocaine = ( 7,4) #this need to be chance munaly for now
        self.BlackKingLocaine = ( 0,4)
        self.inChack = False
        self.pins = []
        self.chacks = []

    def Makemove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--" 
        self.movelog.append(move) #log all the moves in a list
        self.WhiteToMove = not self.WhiteToMove
        #update king move
        if move.pieceMoved == "wK":
            self.WhiteKingLocaine = ( move.endRow,move.endCol)
        elif move.pieceMoved == "bK":
            self.BlackKingLocaine= ( move.endRow,move.endCol)

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop() 
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove
        #update king move
        if move.pieceMoved == "wK":
            self.WhiteKingLocaine = ( move.startRow,move.startCol)
        elif move.pieceMoved == "bK":
            self.BlackKingLocaine= ( move.startRow,move.startCol)

    def getVaildMoves(self):#all moves considering checks
        moves = [] 
        self.inCheck , self.pins , self.checks = self.chackForPinsAndChecks()
        if self.WhiteToMove:
            kingrow = self.WhiteKingLocaine[0]
            kingcol = self.WhiteKingLocaine [1]
        else:
            kingrow = self.BlackKingLocaine [0]
            kingcol - self.BlackKingLocaine [1]

        if self.inCheck:
            if len(self.checks) == 1:# onely one chack
                moves = self.getAllPossibleMoves()
                # to block the check you must move a piece into one of the squares betwenn
                check = self.checks[0] #checkes informion
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #enemy piece cousing the chack
                validSquares = []
                if pieceChecking[1] == "N": # if it a knight so you have move or capure
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingrow + check[2] * i , kingcol + check[3] * i ) #check[2] and check[3] is dericon
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # once you get to the piece, end
                            break
                # get rid of the moves that dont block checks or move king
                for i in range(len(moves)-1, -1, -1): #(range(start, stop, step)) go througth backwards when you are removing from a list 
                    if moves[i].pieceMoved[1] != "k": # move dosent move 
                        if not (moves[i].endRow, moves[i].endCol ) in validSquare: #move dosent block chack or captring piece
                            moves.remove(moves[i])
            else:
                # double check
                self.getKingMoves(kingrow, kingcol, moves)
        else:
            # not in chack so all move are fine 
            moves =  self.getAllPossibleMoves()
        return moves



        


    def chackForPinsAndChecks(Self):
        pins = [] # squares where the allied piend picece and the direction pinned from
        checks = []# squares where enemy is apllyimg chacks
        incheck = False
        if Self.WhiteToMove:
            enemyColor= "b"
            frendlyColor = "w"
            startRow = Self.WhiteKingLocaine[0]
            startCol = Self.WhiteKingLocaine[1]
        else:
            enemyColor= "w"
            frendlyColor = "b"
            startRow = Self.BlackKingLocaine[0]
            startCol = Self.BlackKingLocaine[1]
        # check outward from the king for pines and checks, kepp track of pines
        direction = ((-1,0),(0,-1),(1,0),(0,1), (-1,-1),(-1,1),(1,-1),(1,1)) 
        for j in range(len(direction)):
            d = direction[j]
            possiblePine = () #reast pisbole pines
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0<= endRow < 8 and 0<= endCol < 8: #on board
                    endpice = Self.board[endRow][endCol]
                    if endpice[0] == enemyColor :
                        type = endpice[1]
                        """ 5 posibliteis in this condison
                        1. Perpendicular away from the king so it a rook
                        2. diagonally away from the king the is a bishope
                        3. 1 square away from the king so it a pawn
                        4.any direction so it a queen
                        5. any direction and 1 square away so it a king
                        """
                        if (0 <= j <= 3 and type == "R") or (4<= j <=7 and type == "B" ) or (i == 1 and type == "p"  and ((enemyColor == "w" and 6<= j <= 7) or (enemyColor == "b" and 4<= j <= 5))) or (type == "Q") or (i == 1 and type == "K") :
                            if possiblePine == (): #no piece is blocking so chack
                                incheck = True
                                checks.append( ( endRow, endCol, d[0] , d[1]))
                                break
                            else: #piend
                                pins.append(possiblePine)
                                break
                        else: #enmy piece is not aplyying chacks
                            break
                    elif endpice[0] == frendlyColor:
                        if possiblePine == ():
                            possiblePine = (endRow , endCol , d[0] , d[1])
                        else: #2 frendly pice so not piend
                            break
                else:
                    break
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,2),(1,-2),(2,-1),(2,1))
        for m in knightMoves:
            endRow = startRow + m[0] 
            endCol = startCol + m[1] 
            if 0<= endRow < 8 and 0<= endCol < 8: #on board
                endpiece= Self.board[endRow][endCol]
                if endpice[0] == enemyColor and endpice[1] == "N":
                    incheck = True
                    checks.append( ( endRow, endCol, m[0] , m[1]))
        return incheck , pins , checks


                     



                            





    def getAllPossibleMoves(self):# all moves
        moves = []
        for r  in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.WhiteToMove) or (turn == "b" and not self.WhiteToMove):
                    piece = turn = self.board[r][c][1]
                    self.moveFunciton[piece](r,c , moves)


        return moves


    def getPwanMoves(self, r, c  , moves):#get all the posibels pwan moves in the r , c and add  to the list
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.WhiteToMove:
            if self.board[r-1][c] == "--":#for pygame the start of the white pwan is on row 6 so to go app you need r-1 
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c),(r-1,c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": #first move of the pwan
                        moves.append(Move((r,c),(r-2,c), self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0] == "b":
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r,c),(r-1,c-1), self.board)) #capture to the left
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((r,c),(r-1,c+1), self.board)) #capture to the rigth
        else:
            if self.board[r+1][c] == "--":#for pygame the start of the black pwan is on row 1 so to go app you need r+1 
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c),(r+1,c), self.board))
                    if r == 1 and self.board[r+2][c] == "--": #first move of the pwan
                        moves.append(Move((r,c),(r+2,c), self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0] == "w":
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r,c),(r+1,c-1), self.board)) #capture to the left
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r,c),(r+1,c+1), self.board)) #capture to the rigth





    def getBisopMoves(self, r, c  , moves):#get all the posibels bishop moves in the r , c and add  to the list
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        direction = ((1,1),(1,-1),(-1,-1),(-1,1)) #4 diaganols
        if self.WhiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0<= endRow < 8 and 0<= endCol < 8: #on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endpiece = self.board[endRow][endCol]
                        if endpiece == "--": #empy space valide
                            moves.append(Move((r,c),(endRow,endCol), self.board))
                        elif endpiece[0] == enemyColor:  #enemy space valide
                            moves.append(Move((r,c),(endRow,endCol), self.board))
                            break
                        else: # frendly space incalide
                            break
                else: # out of borad
                    break
    def getKnightMoves(self, r, c  , moves):#get all the posibels knigth moves in the r , c and add  to the list
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,2),(1,-2),(2,-1),(2,1))
        if self.WhiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"
        for m in knightMoves:
            endRow = r + m[0] 
            endCol = c + m[1] 
            if 0<= endRow < 8 and 0<= endCol < 8: #on board
                if not piecePinned:
                    endpiece=self.board[endRow][endCol]
                    if endpiece[0] != allyColor: #not an ally piece (empty or enemy)
                        moves.append(Move((r,c),(endRow,endCol), self.board))

    def getRookMoves(self, r, c  , moves):#get all the posibels rook moves in the r , c and add  to the list\
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                
                if self.board[r][c] != "Q":#cant remove quenn from a pine on a rook move , onely one a bishope moves
                    self.pins.remove(self.pins[i])
                break
        direction = ((1,0),(0,-1),(-1,0),(0,1)) #down left up rigth
        if self.WhiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0<= endRow < 8 and 0<= endCol < 8: #on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endpiece = self.board[endRow][endCol]
                        if endpiece == "--": #empy space valide
                            moves.append(Move((r,c),(endRow,endCol), self.board))
                        elif endpiece[0] == enemyColor:  #enemy space valide
                            moves.append(Move((r,c),(endRow,endCol), self.board))
                            break
                        else: # frendly space incalide
                            break
                else: # out of borad
                    break

    def getQueenMoves(self, r, c  , moves):#get all the posibels queen moves in the r , c and add  to the list
        self.getRookMoves( r, c  , moves)
        self.getBisopMoves( r, c  , moves)
    def getKingMoves(self, r, c  , moves):#get all the posibels king moves in the r , c and add  to the list
        direction = ((1,0),(0,-1),(-1,0),(0,1), (1,1),(1,-1),(-1,-1),(-1,1)) 
        if self.WhiteToMove:
            allayColor = "w"
        else:
            allayColor = "b"
        for d in direction:
            endRow = r + d[0] 
            endCol = c + d[1] 
            if 0<= endRow < 8 and 0<= endCol < 8:
                endpiece = self.board[endRow][endCol]
                if endpiece[0] != allayColor: # not allay piece 
                    if allayColor == " w":
                        self.WhiteKingLocaine = (endRow,endCol)
                    else:
                        self.BlackKingLocaine = (endRow,endCol)
                    inCheck , pins , checks = self.chackForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    if allayColor == " w":
                        self.WhiteKingLocaine = (r,c)
                    else:
                        self.BlackKingLocaine = (r,c)
                


                        





       
  
        


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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        

    def __eq__(self, other):#override equals method 
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False



    def getChessNotiaon(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    def getRankFile(self,r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    







