from abc import ABC, abstractmethod

from discord import Message


class BaseCommand(ABC):
    def __init__(self, message: str):
        self.message = message

    @abstractmethod
    def process(self) -> str:
        raise NotImplementedError

    def strip_prefix(self) -> list[str]:
        return self.message.removeprefix('!gooner')
