
from pybotx import Bot, BotAccountWithSecret, ChatCreatedEvent, HandlerCollector, IncomingMessage

# Создаём объект HandlerCollector
collector = HandlerCollector()




# Обработчик события создания чата
@collector.chat_created
async def handle_chat_created(event: ChatCreatedEvent, bot: Bot) -> None:
    """Обработка события создания чата и отправка приветственного сообщения"""
    await bot.send_message(
        recipients=event.chat.id,
        body="Добро пожаловать! Это приветственное сообщение.",
    )


@collector.default_message_handler
async def default_handler(_: IncomingMessage, bot: Bot) -> None:
    await bot.answer_message("Используйте команду `/help` для получения списка команд.")





# Обработчик команды /commands
@collector.command("/help", description="Выводит список доступных команд")
async def list_commands(message: IncomingMessage, bot: Bot) -> None:
    """Список доступных команд"""
    print("Вызвалась команда help")
    commands = [
        f"{command.name} - {command.description or 'Описание отсутствует'}"
        for command in bot.registry.commands.values()
    ]
    response = "Список доступных команд:\n" + "\n".join(commands)
    await bot.send_message(
        recipients=message.chat.id,
        body=response,
    )


@collector.command(
    "/echo",
    description="Возвращает написанное сообщение",
)
async def echo_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/echo text`

    Reply incoming text after command.

    • `text` - text that should be replied back.
    """
    await bot.answer_message(message.argument)





