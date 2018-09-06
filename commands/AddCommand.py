import os
import re
import tempfile

from commands.AbstractCommand import AbstractCommand
from config.config import API_TOKEN
from models.Location import Location


class AddCommand(AbstractCommand):
    STATE_START = 0
    STATE_NAME = 1
    STATE_IMAGE = 2
    STATE_COORDINATES = 3

    def __init__(self, bot, connection):
        super().__init__(bot, connection)
        self.__previous_state = None
        self.__location = None
        self.reload()

    def process(self, message):
        self.process_next_state(message)

    def process_next_state(self, message):
        result_message = ''
        message_info = self.get_message_info(message)

        if self.__previous_state is None:
            self.increment_step()

            self.get_location().set_user_id(message_info.get_user().get_id())

            result_message = """
                You want add new location. Please write location name:
            """
        elif self.__previous_state == self.STATE_START:
            self.increment_step()
            self.get_location().set_name(message_info.get_text())

            result_message = """Please add location photo or use: \n{}""".format(self.get_cancel_step_commands_text())

        elif self.__previous_state == self.STATE_NAME:
            self.increment_step()
            if message_info.get_file_id() is not None:
                file_info = self.bot.get_file(message_info.get_file_id())
                downloaded_file = self.bot.download_file(file_info.file_path)

                if downloaded_file != '':
                    file_url = os.path.join(tempfile.gettempdir(), '{}.jpg'.format(message_info.get_file_id()))
                    with open(file_url, 'wb') as new_file:
                        new_file.write(downloaded_file)

                    self.get_location().set_photo_url(file_url)

            result_message = """Please add coordinates in format (50.45466, 30.5238) without brackets, where:
                50.45466 - latitude
                30.5238 - longitude
                \n{}""".format(self.get_cancel_step_commands_text())
        elif self.__previous_state == self.STATE_IMAGE:
            location_coordinates = message_info.get_text()
            if self.is_coordinates(location_coordinates) is True:
                latitude, longtitude = location_coordinates.split(',')
                self.get_location().set_latitude(latitude.strip())
                self.get_location().set_longtitude(longtitude.strip())

            self.save(message)

        if result_message != '':
            self.bot.send_message(message_info.get_chat().get_id(), result_message)

    def is_coordinates(self, text):
        result = re.search(r"([0-9]{1,2}).([0-9]+),([\s]{0,})([0-9]{1,2}).([0-9]+)", text)
        return result is not None

    def save(self, message):
        connection = self.connection.get_connection()
        c = connection.cursor()
        c.execute(self.get_location().get_insert_query())
        connection.commit()
        self.connection.close_connection()

        self.bot.send_message(self.get_message_info(message).get_chat().get_id(), 'Location successfully saved')
        self.reload()

    def reload(self):
        self.__previous_state = None
        self.__location = Location()

    def increment_step(self):
        if self.__previous_state is None:
            self.__previous_state = self.STATE_START
        elif self.__previous_state == self.STATE_START:
            self.__previous_state = self.STATE_NAME
        elif self.__previous_state == self.STATE_NAME:
            self.__previous_state = self.STATE_IMAGE
        elif self.__previous_state == self.STATE_IMAGE:
            self.__previous_state = self.STATE_COORDINATES
        else:
            self.reload()

    def get_location(self) -> Location:
        return self.__location

    def get_cancel_step_commands_text(self):
        return """
            /next_step - got to next step of current command
            /cancel - for cancel add new location
        """