from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class GameRule:
    name: str
    max_score: int
    acceptable_chars: list[str]
