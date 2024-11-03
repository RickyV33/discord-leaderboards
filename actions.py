from enum import Enum


class Actions(Enum):
    RUN = "run"
    INIT_DB = "init_db"
    BACKFILL = "backfill"

    @classmethod
    def parse(cls, action_str: str):
        try:
            return cls(action_str)
        except ValueError:
            raise ValueError(
                f"'{action_str}' is not a valid action. Try: {[action.value for action in Actions]}"
            )
