from commands.AbstractCommand import AbstractCommand
from models.Location import Location


class ResetCommand(AbstractCommand):
    def process(self, message):
        message_info = self.get_message_info(message)
        connection = self.connection.get_connection()
        c = connection.cursor()
        c.execute(Location.get_delete_by_user_id_query(message_info.get_user().get_id()))
        self.connection.close_connection()
        self.bot.send_message(
            self.get_message_info(message).get_chat().get_id(),
            'Your list was successfully clean. You can /add new location.'
        )