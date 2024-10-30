from dataclasses import dataclass

from rules.game_rule import GameRule


class GameRuleFetcher:
    def __init__(self, rules: list[GameRule]):
        self.rules = rules


    def get_rules(self, name: str) -> GameRule:
        for rule in self.rules:
            if rule.name == name:
                return rule
        raise Exception(f"Rule not found: {name}")