import sqlite3
import user

class UsersDatabase:
    database_name="users.sqlite"
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    def __init__(self):
        self.create_tables()

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

    def update_user(self, username, elo, puzzles_solved):
        self.cursor.execute("UPDATE user SET elo=?, puzzles_solved=? WHERE username=?",
                            (elo, puzzles_solved, username))
        self.conn.commit()

    def check_if_username_exists(username):
        UsersDatabase.cursor.execute("SELECT COUNT(*) FROM user WHERE username=?", (username,))
        count = UsersDatabase.cursor.fetchone()[0]
        return count > 0 # აბრუნებს True ან False იმის მიხედვით username არსებობს ბაზაში თუ არა.

    def return_user_as_class(self, username):
        UsersDatabase.cursor.execute("SELECT * FROM user WHERE username=?", (username,))
        data = UsersDatabase.cursor.fetchone()
        current_user = user.User(data[1], data[2], data[3])
        return current_user

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM user WHERE username=?", (username,))
        self.conn.commit()
