from abc import ABC, abstractmethod

from discord import Message


class BaseCommand(ABC):
    @abstractmethod
    def process(self) -> str:
        raise NotImplementedError
