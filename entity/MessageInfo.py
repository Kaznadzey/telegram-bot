from entity.ChatInfo import ChatInfo
from entity.ChatUser import ChatUser


class MessageInfo:
    def __init__(self, message):
        self.__user = ChatUser(message.from_user)
        self.__chat = ChatInfo(message.chat)
        self.__text = message.text
        self.__file_id = None
        if message.photo is not None:
            self.__file_id = message.photo[-1].file_id

    def get_chat(self):
        return self.__chat

    def get_user(self):
        return self.__user

    def get_text(self):
        return self.__text

    def get_file_id(self):
        return self.__file_id
