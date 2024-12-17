from datetime import datetime

import pytz

from channels.timeframe import Timeframe
from channels.total_scores import TotalScores, UserScore
from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User
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
        user_db_api: User,
        channel_db_api: Channel,
    ) -> None:
        self.server_id = server_id
        self.game_db_api: Game = game_db_api
        self.score_db_api: Score = score_db_api
        self.user_db_api: User = user_db_api
        self.channel_db_api: Channel = channel_db_api
        self.game_api_provider: GameApiProvider = game_api_provider

    def get(
        self, game_type: GameType, timeframe: Timeframe = Timeframe.ALL
    ) -> TotalScores:
        game = self.game_db_api.get_or_none(name=game_type.value)
        total_possible = self._get_total_possible_points(game, timeframe)
        rounds = self._total_rounds_played(game, timeframe)
        return TotalScores(
            users=self._get_user_scores(game, timeframe),
            total_score=total_possible,
            total_rounds=rounds,
            timeframe=timeframe,
            game=game_type,
        )

    def _get_user_scores(self, game: Game, timeframe: Timeframe) -> list[UserScore]:
        round_lower_bound = self._get_round_lower_bound(game, timeframe)
        channels = self.channel_db_api.select().where(
            Channel.discord_server_id == self.server_id
        )
        scores = (
            self.score_db_api.select()
            .where(
                Score.game == game,
                Score.round > round_lower_bound,
                Score.channel.in_(channels),
            )
            .execute()
        )
        scores_by_user: dict[User, list[Score]
                             ] = self._populate_scores_by_user(scores)
        return [
            UserScore(
                username=str(user.discord_name),
                completed=len(scores),
                scored=sum(score.score for score in scores),
                total_completed_score=len(scores) * self.game_api_provider.provide(
                    GameType(game.name)
                ).max_score(),
            )
            for user, scores in scores_by_user.items()
        ]

    def _populate_scores_by_user(self, scores: list[Score]) -> dict[User, list[Score]]:
        scores_by_user: dict[User, list[Score]] = {}
        for score in scores:
            if score.user not in scores_by_user:
                scores_by_user[score.user] = []
            scores_by_user[score.user].append(score)
        return scores_by_user

    def _total_rounds_played(self, game: Game, timeframe: Timeframe) -> int:
        current_round = self._get_current_round(game)
        round_lb = self._get_round_lower_bound(game, timeframe)
        total_rounds = current_round - round_lb
        return total_rounds

    def _get_total_possible_points(self, game: Game, timeframe: Timeframe) -> int:
        game_api = self.game_api_provider.provide(GameType(game.name))
        max_score = game_api.max_score()
        total_possible = max_score * self._total_rounds_played(game, timeframe)
        return total_possible

    def _get_current_round(self, game: Game) -> int:
        today_in_pacific: datetime = datetime.now(pytz.timezone("US/Pacific"))
        days_since_anchor = (today_in_pacific.date() - game.date_anchor).days
        current_round = days_since_anchor + game.round_anchor
        return current_round

    def _get_round_lower_bound(self, game: Game, timeframe: Timeframe) -> int:
        # NON INCLUSIVE

        if timeframe == Timeframe.ALL:
            return 0  # The first round

        return self._get_current_round(game) - timeframe.to_days()
