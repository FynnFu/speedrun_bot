from speedrun_bot import Bot
from threading import Thread

if __name__ == '__main__':
    # создание и запуск обычного бота
    bot = Bot()
    bot.run_long_poll()
