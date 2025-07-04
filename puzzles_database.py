import sqlite3
from puzzle import Puzzle
from random import *

class PuzzlesDatabase:
    def __init__(self, database_name="data.sqlite"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def get_all_puzzles(self):
        self.cursor.execute("SELECT * FROM lichess_puzzle_transformed WHERE Themes LIKE ?", ('%mateIn%',))
        return self.cursor.fetchall()

    def get_random_puzzle(self):
        puzzles = self.get_all_puzzles()
        random_puzzle = puzzles[randint(0, len(puzzles)-1)]

        puzzle_id = random_puzzle[0]
        fen = random_puzzle[2]
        moves = random_puzzle[3]
        rating = random_puzzle[4]

        puzzle = Puzzle(puzzle_id, fen, moves, rating)
        return puzzle