from uuid import UUID

from fastapi import FastAPI
from pybotx import Bot, BotAccountWithSecret, ChatCreatedEvent, HandlerCollector, IncomingMessage
from app.api.routers import router
#from bot import bot [разобраться с коллекторами]



# Создаём объект HandlerCollector
collector = HandlerCollector()

bot = Bot(
    collectors=[collector],
    bot_accounts=[
        BotAccountWithSecret(
            # Не забудьте заменить эти учётные данные на настоящие,
            # когда создадите бота в панели администратора.
            id=UUID("123e4567-e89b-12d3-a456-426655440000"),
            cts_url="http://127.0.0.1:8000",
            secret_key="e29b417773f2feab9dac143ee3da20c5",
        ),
    ],
)

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
    commands = [
        f"{command.name} - {command.description or 'Описание отсутствует'}"
        for command in bot.registry.commands.values()
    ]
    response = "Список доступных команд:\n" + "\n".join(commands)
    await bot.send_message(
        recipients=message.chat.id,
        body=response,
    )


@collector.command_with_help(
    "/echo",
    description="Возвращает написанное сообщение",
)
async def echo_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/echo text`

    Reply incoming text after command.

    • `text` - text that should be replied back.
    """
    await bot.answer_message(message.argument)













async def startup() -> None:
    await bot.startup()



def get_application() -> FastAPI:
    """Create configured server application instance."""
    application = FastAPI(title="bot")
    application.state.bot = bot

    application.add_event_handler("startup", startup)
    application.add_event_handler("shutdown", bot.shutdown)

    application.include_router(router)

    return application



app = get_application()






