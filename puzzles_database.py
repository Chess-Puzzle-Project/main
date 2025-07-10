import sqlite3, ui
from puzzle import Puzzle
from random import *

class PuzzlesDatabase:
    next_rating = None
    def __init__(self, database_name="data.sqlite"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def get_all_puzzles(self):
        self.cursor.execute("SELECT * FROM lichess_puzzle_transformed")
        return self.cursor.fetchall()

    def get_random_puzzle(self):
        puzzles = self.get_all_puzzles()
        random_puzzle = puzzles[randint(0, len(puzzles)-1)]

        puzzle_id = random_puzzle[0]
        fen = random_puzzle[1]
        moves = random_puzzle[2]
        rating = random_puzzle[3]

        puzzle = Puzzle(puzzle_id, fen, moves, rating)
        return puzzle

    def get_next_puzzle(self):
        puzzles = self.get_all_puzzles()
        user = ui.MainWindow.CURRENT_USER
        user_elo = user.elo

        all_ratings = []
        for puzzle in puzzles:
            all_ratings.append(int(puzzle[3]))
        all_ratings.sort()
        all_ratings = list(set(all_ratings))

        puzzle_ids_grouped = {}
        puzzles_by_rating = {}
        for puzzle in puzzles:
            rating = int(puzzle[3])
            if rating not in puzzles_by_rating:
                puzzles_by_rating[rating] = []
            puzzles_by_rating[rating].append(puzzle[0])

        for rating in all_ratings:
            puzzle_ids_grouped[rating] = puzzles_by_rating.get(int(rating), [])

        for rating in all_ratings:
            if int(rating) > user_elo and int(rating) > 550:
                next_puzzle_id = choice(puzzle_ids_grouped[rating])
                print(next_puzzle_id)
                break

        next_puzzle = None
        for puzzle in puzzles:
            if puzzle[0] == next_puzzle_id:
                PuzzlesDatabase.next_rating = int(puzzle[3])
                next_puzzle = Puzzle(puzzle[0], puzzle[1], puzzle[2], puzzle[3])
                break
        print(next_puzzle)

        return next_puzzle
