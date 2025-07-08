class User:
    def __init__(self, user_id, username, elo, puzzles_solved):
        self.user_id = user_id
        self.username = username
        self.elo = elo
        self.puzzles_solved = puzzles_solved

    # აბრუნებს tuple-ს რო users_database ბაზაში პირდაპირ შეგვეძლოს ახალი user-ის დამატება:
    # მაგალითად: database.add_user(User) ანუ პირდაპირ რო გადაეცეს User კლასი.
    def __str__(self):
        return (self.username, self.elo, self.puzzles_solved)