import json

import vk_api  # использование VK API
from vk_api import keyboard
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id  # снижение количества повторных отправок сообщения
from dotenv import load_dotenv  # загрузка информации из .env-файла
import os  # работа с файловой системой


class Bot:
    """
    Базовый класс бота ВКонтакте
    """

    token = None

    # текущая сессия ВКонтакте
    vk_session = None

    # API текущей сессии ВКонтакте
    session_api = None

    # длительное подключение
    long_poll = None

    def __init__(self):
        """
        Инициализация бота при помощи получения доступа к API ВКонтакте
        """
        # загрузка информации из .env-файла
        load_dotenv()

        token = os.getenv("token")

        # авторизация
        vk_session = vk_api.VkApi(token=token)

        session_api = vk_session.get_api()

        long_poll = VkLongPoll(vk_session)

    def get_but(self):
        return {"action": {"type": "location", "payload": ""}}

    def geo(self):
        result = self.vk_session.method(
            "messages.getById",
            {"message_ids": [self.message_id], "group_id": 189072320}
        )
        geo = result['items'][0]['geo']['coordinates']
        latitude, longitude = geo['latitude'], geo['longitude']
        return (latitude, longitude)

    def send_messages(self, user_id, messages):
        try:
            self.vk_session.method(
                'messages.send',
                {'user_id': user_id,
                 'message': messages,
                 'random_id': get_random_id(),
                 'keyboard': keyboard}
            )
            print(f"Сообщение отправлено для ID {user_id} с текстом: {messages}")
        except Exception as error:
            print("msg_err: " + str(error))

    def get_username(self, user_id):
        user_info = self.session_api.users.get(user_ids=user_id)[0]
        username = '{} {}'.format(
            user_info['first_name'],
            user_info['last_name']
        )
        return f'[id{id}|{username}]'

    # def get_but(text, color):
    #     return {
    #         "action": {
    #             "type": "text",
    #             "payload": "{\"button\": \"" + "1" + "\"}",
    #             "label": f"{text}"
    #         },
    #         "color": f"{color}"
    #     }

    keyboard = {
        "buttons": [
            # [
            #     {
            #         "action": {
            #             "type": "callback",
            #             "label": "label",
            #             "payload": ""
            #         },
            #         "color": "primary"
            #     }
            # ],
            [
                {
                    "action": {
                        "type": "location",
                        "payload": ""
                    }
                }

            ],
            [
                {
                    'action': {
                        'type': "callback",
                        'payload': "{}",
                        'label': "Нажми меня"
                    }
                }
            ],
            [
                {
                    'action': {
                        "type": "show_snackbar",
                        "text": "Покажи исчезающее сообщение на экране"
                    }
                }
            ]
        ],
        "inline": False
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    def run_long_poll(self):
        """
        Запуск бота
        """
        print("Запуск бота")
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    msg = event.text.lower()
                    user_id = event.user_id
                    print(msg)
                    self.send_messages(user_id, 'привет')

