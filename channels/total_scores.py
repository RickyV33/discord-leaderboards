from dataclasses import dataclass

from channels.timeframe import Timeframe
from games.game_type import GameType

from table2ascii import table2ascii as t2a, PresetStyle


@dataclass(kw_only=True, frozen=True)
class UserScore:
    username: str
    completed: int
    scored: int

    def __str__(self) -> str:
        return f"UserScore(username={self.username}, completed={self.completed}, scored={self.scored})"

    def to_discord_message(self) -> str:
        return t2a(
            [
                ["Username", "Completed", "Scored"],
                [self.username, self.completed, self.scored],
            ],
            style=PresetStyle.double,
        )


@dataclass(kw_only=True, frozen=True)
class TotalScores:
    users: list[UserScore]
    total_rounds: int
    total_score: int
    timeframe: Timeframe
    game: GameType

    def to_discord_message(self) -> str:
        ranked_users = sorted(self.users, key=lambda user: user.scored, reverse=True)
        table = t2a(
            header=[
                "Rank",
                "Username",
                "Completed",
                "% Completed",
                "Scored",
                "% Scored of Total",
            ],
            body=[
                [
                    i + 1,
                    user.username,
                    user.completed,
                    round(user.completed / self.total_rounds * 100, 2)
                    if self.total_rounds
                    else 0,
                    user.scored,
                    round(user.scored / self.total_score * 100, 2)
                    if self.total_score
                    else 0,
                ]
                for i, user in enumerate(ranked_users)
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )
        return f"```\n{self.game.value.capitalize()}\nTotal Rounds Possible: {self.total_rounds}\nTotal Points Possible: {self.total_score}\n{table}\n```"
