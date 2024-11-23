from datetime import date, timedelta
from dataclasses import dataclass

from channels.timeframe import Timeframe
from games.game_type import GameType

from table2ascii import table2ascii as t2a, PresetStyle


@dataclass(kw_only=True, frozen=True)
class UserScore:
    username: str
    completed: int
    scored: int
    total_completed_score: int

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
        table = t2a(
            header=[
                "Rank",
                "Username",
                "Completed",
                "Scored",
                "% Scored of Completed"
            ],
            body=self.get_body(),
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )
        return f"```\n{self.game.value.capitalize()}\nTotal Rounds Possible: {self.total_rounds}\nTotal Points Possible: {self.total_score}\n{table}\n```"

    def to_mobile_discord_message(self) -> str:
        body = self.get_body()
        """
        [
            ["Rank", "Username", "Completed", "Scored", "% Scored of Completed"],
            [1, "user1", "10 (100%)", "10 (100%)", "100%"],
        ]
        """
        """
            Total Points Possible: 10
            Total Rounds Possible: 10
            Timeframe: a week ago
            * #1: 
              * User: **user1**
              * **Completed**: 10 (100%)
              * **Scored**: 10 (100%)
              * **% Scored of Completed**: 100%
        """
        as_message = f"**Total Rounds Possible**: {self.total_rounds}\n"
        as_message += f"**Total Points Possible**: {self.total_score}\n"
        as_message += f"**Timeframe**: {self.timeframe.human_readable}\n"
        for user in body:
            as_message += f"* **#{user[0]}**\n"
            as_message += f"  * **User**: {user[1]}\n"
            as_message += f"  * **Completed**: {user[2]}\n"
            as_message += f"  * **Scored**: {user[3]}\n"
            as_message += f"  * **% Scored of Completed**: {user[4]}%\n"

        return as_message

    def get_body(self):
        ranked_users = sorted(
            self.users, key=lambda user: user.scored, reverse=True)
        items = []
        for i, user in enumerate(ranked_users):
            completed_percentage = round(
                user.completed / self.total_rounds * 100, 2) if self.total_rounds else 0
            scored_percentage = round(
                user.scored / self.total_score * 100, 2) if self.total_score else 0

            item = [
                i + 1,
                user.username,
                f"{user.completed} ({completed_percentage}%)",
                f"{user.scored} ({scored_percentage}%)",
                round(user.scored / user.total_completed_score *
                      100, 2) if user.total_completed_score else 0
            ]
            items.append(item)

        return items
