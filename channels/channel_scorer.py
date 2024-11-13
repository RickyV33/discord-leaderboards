from datetime import datetime
from discord import Message

from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User
from games.game_api_provider import GameApiProvider
from games.game_type import GameType


class ChannelScorer:
    def __init__(
        self,
        *,
        channel_id: str,
        game_db_api: Game,
        score_db_api: Score,
        channel_db_api: Channel,
        user_db_api: User,
        game_api_provider: GameApiProvider,
    ) -> None:
        self.channel_id = channel_id
        self.game_api_provider = game_api_provider
        self.game_db_api: Game = game_db_api
        self.score_db_api: Score = score_db_api
        self.channel_db_api: Channel = channel_db_api
        self.user_db_api: User = user_db_api

    def score(self, message: Message) -> tuple[int, bool]:
        game_api = self.game_api_provider.provide(self._get_game_name())
        if not game_api.is_valid(message.content):
            raise Exception(f"Unable to score message: {message.id}")
        discord_user_id = message.author.id
        game_score = game_api.score(message.content)
        round = game_api.round(message.content)
        user, _ = self.user_db_api.get_or_create(
            discord_user_id=discord_user_id,
            discord_name=message.author.name,
        )
        channel = self.channel_db_api.get_or_none(self.channel_id)
        game = self._get_game()
        exists = (
            self.score_db_api.select()
            .where(
                Score.user == user,
                Score.round == round,
                Score.game == game.id,
            )
            .get_or_none()
        )

        if exists:
            print(f"Score already exists for user: {
                  user.discord_name}, round: {round}, game: {game.name}")
            return exists.score, False

        message.created_at.astimezone(datetime.now().astimezone().tzinfo)
        self.score_db_api.insert(
            user_id=user,
            game_id=game.id,
            score=game_score,
            round=round,
            channel=channel,
            discord_message_id=message.id,
            date_submitted=message.created_at,
        ).on_conflict_replace().execute()

        return game_score, True

    def get_reaction(self) -> str:
        game_api = self.game_api_provider.provide(self._get_game_name())
        return game_api.get_reaction()

    def _get_game(self) -> Game:
        game: Game = self.channel_db_api.get_or_none(self.channel_id).game
        return game

    def _get_game_name(self) -> GameType:
        return GameType(self._get_game().name)

    def last_scored_game(self) -> Score:
        result = (
            self.score_db_api.select()
            .join(Game)
            .where(Game.name == self._get_game_name().value)
            .order_by(Score.date_submitted.desc())
            .get_or_none()
        )

        return result
