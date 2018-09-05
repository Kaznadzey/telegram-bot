from commands.AbstractCommand import AbstractCommand
from config.config import BOT_NAME


class WelcomeCommand(AbstractCommand):
    def process(self, message):
        message_info = self.get_message_info(message)

        welcome_message = """
               Hello {}! My name is {}, and I allow you save your favorite locations for feature visit.
               \nYou can use my commands menu for fast access to all my opportunities.
               \nHere is basic commands:
               /add - Allow you add new location
               /list - Display list of saved locations
               /reset - Remove all previously saved locations 
           """.format(message_info.get_user().get_first_name(), BOT_NAME)

        self.bot.send_message(message_info.get_chat().get_id(), welcome_message)