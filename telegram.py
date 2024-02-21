from configparser import ConfigParser
from pyrogram.client import Client
from plate import Plate
from database import Database


class EyezmiediaBot(Client):
    def __init__(self):
        name = 'TeleShops'
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.database = Database()

        self.plate = Plate(
            root=self.config['plate']['root'],
            fallback=self.config['plate']['fallback']
        )

        super().__init__(
            name,
            api_id=int(self.config['pyrogram']['api_id']),
            api_hash=self.config['pyrogram']['api_hash'],
            bot_token=self.config['pyrogram']['bot_token'],
            plugins=dict(root="plugins"),

            workers=16,
            workdir='sessions/'

        )
        print('Bot started successfully')
