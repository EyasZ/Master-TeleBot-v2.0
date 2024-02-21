import logging
from telegram import EyezmiediaBot


if __name__ == '__main__':
    logging.basicConfig(
        filename='app.log',
        filemode='w',
        format='[%(asctime)s] [%(levelname)s] - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.WARNING
    )

    EyezmiediaBot().run()
