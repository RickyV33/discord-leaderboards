from datetime import datetime
from discord import Message
from typing import Any

from channels.timeframe import Timeframe
from channels.total_scores import TotalScores, UserScore
from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User
from games.game_api import GameApi
from games.game_api_provider import GameApiProvider
from games.game_type import GameType


class ScoreFetcher:
    def __init__(
        self,
        *,
        server_id: str,
        game_api_provider: GameApiProvider,
        game_db_api: Game,
        score_db_api: Score,
        user_db_api: User
    ) -> None:
        self.server_id = server_id
        self.game_db_api: Game = game_db_api
        self.score_db_api: Score = score_db_api
        self.user_db_api: User = user_db_api
        self.game_api_provider: GameApiProvider = game_api_provider

    def get(self, game_type: GameType, timeframe: Timeframe = Timeframe.ALL) -> TotalScores:
        game = self.game_db_api.get_or_none(name=game_type)
        total_possible = self._get_total_possible(game, timeframe)
        return TotalScores(
            users=self._get_user_scores(game, timeframe),
            total_possible=total_possible,
            timeframe=timeframe,
            game=game_type,
            with_missing=False
        )

    def _get_user_scores(self, game: Game, timeframe: Timeframe) -> list[UserScore]:
        date_lower_bound = timeframe.datetime
        scores = self.score_db_api.select().where(
            Score.game == game,
            Score.date_submitted >= date_lower_bound if timeframe != Timeframe.ALL else True  # type: ignore
        )
        scores_by_user: dict[User, list[Score]
                             ] = self._populate_scores_by_user(scores)
        return [
            UserScore(
                username=str(user.discord_name),
                completed=len(scores),
                scored=sum(score.score for score in scores)  # type: ignore
            ) for user, scores in scores_by_user.items()
        ]

    def _populate_scores_by_user(self, scores: list[Score]) -> dict[User, list[Score]]:
        scores_by_user = {}
        for score in scores:
            if score.user not in scores_by_user:
                scores_by_user[score.user] = []
            scores_by_user[score.user].append(score)
        return scores_by_user

    def _get_total_possible(self, game: Game, timeframe: Timeframe) -> int:
        game_api = self.game_api_provider.provide(GameType(game.name))
        max_score = game_api.max_score()
        if timeframe != Timeframe.ALL:
            total_possible = max_score * timeframe.to_days
        else:
            oldest_score = self.score_db_api.select().where(
                Score.game == game
            ).order_by(Score.date_submitted).first()
            days_since_oldest = (
                datetime.now() - oldest_score.date_submitted).days
            total_possible = max_score * days_since_oldest

        return total_possible
