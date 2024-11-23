from abc import ABC, abstractmethod

from discord import Message


class BaseCommand(ABC):
    @abstractmethod
    def process(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def process_mobile(self) -> str:
        raise NotImplementedError
