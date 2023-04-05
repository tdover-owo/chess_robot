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
    