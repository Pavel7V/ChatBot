import base64
import hashlib
import hmac
import datetime
from uuid import UUID

import httpx
import jwt
from pybotx import Bot, BotAccountWithSecret, ChatCreatedEvent, HandlerCollector, IncomingMessage

from app.bot.commands import command_main
import asyncio




bot = Bot(
    collectors=[command_main.collector],
    bot_accounts=[
        BotAccountWithSecret(
            # Не забудьте заменить эти учётные данные на настоящие,
            # когда создадите бота в панели администратора.
            id=UUID("8dada2c8-67a6-4434-9dec-570d244e78ee"),
            cts_url="http://127.0.0.1:8000",
            secret_key="e29b417773f2feab9dac143ee3da20c5",
        ),
    ],
)

#генерация тестового токена
id_bot = "8dada2c8-67a6-4434-9dec-570d244e78ee"
key_secret = "e29b417773f2feab9dac143ee3da20c5"
signature = hmac.new(
    key=key_secret.encode(),
    msg=id_bot.encode(),
    digestmod=hashlib.sha256
).digest()

signature = base64.b16encode(signature).decode()
print(f"Generated token: {signature}")



payload = {
        "bot_id": id_bot,
        "aud": [id_bot],                           # Добавляем аудиенцию (bot_id в виде списка)
        "iss": bot._bot_accounts_storage.get_bot_account(UUID(id_bot)).host,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Срок действия токена (1 час)
        "iat": datetime.datetime.utcnow(),                      # Время выдачи токена
        "permissions": ["send_message", "get_chats"]   # Пример прав
    }
print(bot._bot_accounts_storage.get_bot_account(UUID(id_bot)).host)

token = jwt.encode(payload, key_secret, algorithm="HS256")
print(token)


