class ChatUser:
    def __init__(self, info):
        self.__id = info.id
        self.__first_name = info.first_name

    def get_id(self):
        return self.__id

    def get_first_name(self):
        return self.__first_name