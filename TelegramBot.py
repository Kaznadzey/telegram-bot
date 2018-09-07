import time

import telebot

from DbConnection import DbConnection
from commands.AddCommand import AddCommand
from commands.ListCommand import ListCommand
from commands.ResetCommand import ResetCommand
from commands.WelcomeCommand import WelcomeCommand
from config.config import API_TOKEN
from entity.MessageInfo import MessageInfo


class TelegramBot:
    def __init__(self):
        self.bot = self.create_bot()
        self.connection = DbConnection()
        self.commands = {
            'add': AddCommand(self.bot, self.connection),
            'list': ListCommand(self.bot, self.connection),
            'reset': ResetCommand(self.bot, self.connection),
            'start': WelcomeCommand(self.bot, self.connection)
        }
        self.current_command = None
        self.register_commands(self.bot)

    def create_bot(self):
        app = telebot.TeleBot(token=API_TOKEN)

        return app

    def register_commands(self, bot):
        @self.bot.message_handler(commands=['add'])
        def add_command_handler(message):
            self.current_command = 'add'
            self.commands['add'].reload()
            self.commands['add'].process(message)

        @self.bot.message_handler(content_types=['photo'])
        def add_photo_to_location(message):
            self.current_command = 'add'
            self.commands['add'].process_next_state(message)

        @self.bot.message_handler(commands=['list'])
        def list_command_handler(message):
            self.current_command = 'list'
            self.commands['list'].process(message)

        @self.bot.message_handler(commands=['reset'])
        def reset_command_handler(message):
            self.current_command = 'reset'
            self.commands['reset'].process(message)

        @self.bot.message_handler(commands=['start'])
        def start_command_handler(message):
            self.current_command = 'start'
            self.commands['start'].process(message)

        @self.bot.message_handler(commands=['next_step'])
        def next_step_command_handler(message):
            if self.current_command == 'add':
                self.commands['add'].process_next_state(message)

        @self.bot.message_handler(commands=['cancel'])
        def cancel_command_handler(message):
            if self.current_command == 'add':
                self.commands['add'].reload()

            self.current_command = None
            self.bot.send_message(message.chat.id, 'Command cancelled!')

        @self.bot.message_handler()
        def message_handler(message):
            if self.current_command == 'add':
                self.commands['add'].process_next_state(message)
            else:
                message_info = MessageInfo(message)
                bot.send_message(message_info.get_chat().get_id(), message_info.get_text())

    def run(self):
        while True:
            try:
                self.bot.polling()
            except Exception:
                time.sleep(10)