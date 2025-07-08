import sqlite3

class UsersDatabase:
    def __init__(self, database_name="users.sqlite"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        # print(self.check_if_username_exists("temokhvedelidze"))
        # print(self.check_if_username_exists("random_username"))

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                elo INTEGER NOT NULL,
                puzzles_solved INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def add_user(self, username, elo, puzzles_solved):
        self.cursor.execute("INSERT INTO user (username, elo, puzzles_solved) VALUES (?, ?, ?)",
                            (username, elo, puzzles_solved))
        self.conn.commit()

    def update_user(self, user_id, username, elo, puzzles_solved):
        self.cursor.execute("UPDATE user SET username=?, elo=?, puzzles_solved=? WHERE id=?",
                            (username, elo, puzzles_solved, user_id))
        self.conn.commit()

    def check_if_username_exists(self, username):
        self.cursor.execute("SELECT COUNT(*) FROM user WHERE username=?", (username,))
        count = self.cursor.fetchone()[0]
        return count > 0 # აბრუნებს True ან False იმის მიხედვით username არსებობს ბაზაში თუ არა.