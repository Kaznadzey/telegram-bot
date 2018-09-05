from abc import ABCMeta, abstractmethod

from DbConnection import DbConnection
from entity.MessageInfo import MessageInfo


class AbstractCommand(metaclass=ABCMeta):
    def __init__(self, bot, connection:DbConnection):
        self.bot = bot
        self.connection = connection

    def get_message_info(self, message) -> MessageInfo:
        return MessageInfo(message)

    @abstractmethod
    def process(self, message):
        pass
