from games import GameApi


class GameApiProvider:
    def __init__(self, apis: list[GameApi]):
        self.apis = apis


    def get_api(self, name: str) -> GameApi:
        for api in self.apis:
            if api.name == name:
                return 
        raise Exception(f"Rule not found: {name}")