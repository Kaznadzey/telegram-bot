from commands.AbstractCommand import AbstractCommand
from models.Location import Location


class ListCommand(AbstractCommand):
    def process(self, message):
        message_info = self.get_message_info(message)
        connection = self.connection.get_connection()
        c = connection.cursor()
        c.execute(Location.get_find_by_user_id_query(message_info.get_user().get_id()))
        locations = c.fetchall()
        self.connection.close_connection()

        chat_id = message_info.get_chat().get_id()

        if len(locations) > 0:
            for location in locations:
                self.bot.send_message(chat_id, location[1])
                if location[2] != 'None' and location[2] != '':
                    image = open(location[2], 'rb')

                    self.bot.send_photo(chat_id, image, caption="Photo '{}'".format(location[1]))

                latitude = int(location[3])
                longtitude = int(location[4])

                if latitude > 0 or longtitude > 0:
                    self.bot.send_location(chat_id, latitude, longtitude)
        else:
            self.bot.send_message(chat_id, 'Locations list is empty. You can /add your first location.')
