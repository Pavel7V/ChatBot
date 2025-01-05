#pytest -v
import pytest

from app.main import get_application

from http import HTTPStatus
from typing import Dict
from uuid import UUID

import respx
from fastapi.testclient import TestClient
from pybotx import Bot

import logging
from http import HTTPStatus
from typing import Any, AsyncGenerator, Callable, Generator, List, Optional
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import httpx
import pytest
import respx
#from alembic import config as alembic_config
from asgi_lifespan import LifespanManager
from pybotx import (
    Bot,
    BotAccount,
    Chat,
    ChatTypes,
    IncomingMessage,
    MentionList,
    UserDevice,
    UserSender,
    lifespan_wrapper,
)
from pybotx.logger import logger
from pybotx.models.attachments import IncomingFileAttachment
#from pybotx_fsm import FSM
#from sqlalchemy.ext.asyncio import AsyncSession

#from app.caching.redis_repo import RedisRepo
from app.main import get_application
#from app.settings import settings

@pytest.fixture
def bot_id() -> UUID:
    return UUID("123e4567-e89b-12d3-a456-426655440000")


@pytest.fixture
def host() -> str:
    return "http://127.0.0.1:8000"


@pytest.fixture
def user_huid() -> UUID:
    return "e29b417773f2feab9dac143ee3da20c5"

def mock_authorization() -> None:
    respx.route(method="GET", path__regex="/api/v2/botx/bots/.*/token").mock(
        return_value=httpx.Response(
            HTTPStatus.OK,
            json={
                "status": "ok",
                "result": "token",
            },
        ),
    )

@pytest.fixture
async def bot(
    respx_mock: Callable[..., Any],  # We can't apply pytest mark to fixture
) -> AsyncGenerator[Bot, None]:
    fastapi_app = get_application()

    mock_authorization()

    async with LifespanManager(fastapi_app):
        built_bot = fastapi_app.state.bot

        built_bot.answer_message = AsyncMock(return_value=uuid4())
        built_bot.send = AsyncMock(return_value=uuid4())

        yield built_bot


@respx.mock
def test__web_app__bot_status_response_ok(
    bot_id: UUID,
    bot: Bot,
) -> None:
    # - Arrange -
    query_params = {
        "bot_id": str(bot_id),
        "chat_type": "chat",
        "user_huid": "f16cdc5f-6366-5552-9ecd-c36290ab3d11",
    }

    # - Act -
    with TestClient(get_application()) as test_client:
        response = test_client.get(
            "/status",
            params=query_params,
        )

    # - Assert -
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "result": {
            "commands": [
                {
                    "body": "/help",
                    "description": "Выводит список доступных команд",
                    "name": "/help",
                },
                {
                    "body": "/echo",
                    "description": "Возвращает написанное сообщение",
                    "name": "/echo",
                },

            ],
            "enabled": True,
            "status_message": "Bot is working",
        },
        "status": "ok",
    }


# @respx.mock
# def test__web_app__bot_status_unknown_bot_response_service_unavailable(
#     bot_id: UUID,
#     bot: Bot,
# ) -> None:
#     # - Arrange -
#     query_params = {
#         "bot_id": "f3e176d5-ff46-4b18-b260-25008338c06e",
#         "chat_type": "chat",
#         "user_huid": "f16cdc5f-6366-5552-9ecd-c36290ab3d11",
#     }
#
#     # - Act -
#     with TestClient(get_application()) as test_client:
#         response = test_client.get(
#             "/status",
#             params=query_params,
#         )
#
#     # - Assert -
#     assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
#
#     status_message = response.json()["error_data"]["status_message"]
#     assert status_message == "Unknown bot_id: f3e176d5-ff46-4b18-b260-25008338c06e"
#
#
#
# @respx.mock
# def test__web_app__unknown_bot_response_service_unavailable(
#     bot: Bot,
# ) -> None:
#     # - Arrange -
#     payload = {
#         "bot_id": "c755e147-30a5-45df-b46a-c75aa6089c8f",
#         "command": {
#             "body": "/debug",
#             "command_type": "user",
#             "data": {},
#             "metadata": {},
#         },
#         "attachments": [],
#         "async_files": [],
#         "entities": [],
#         "source_sync_id": None,
#         "sync_id": "6f40a492-4b5f-54f3-87ee-77126d825b51",
#         "from": {
#             "ad_domain": None,
#             "ad_login": None,
#             "app_version": None,
#             "chat_type": "chat",
#             "device": None,
#             "device_meta": {
#                 "permissions": None,
#                 "pushes": False,
#                 "timezone": "Europe/Moscow",
#             },
#             "device_software": None,
#             "group_chat_id": "30dc1980-643a-00ad-37fc-7cc10d74e935",
#             "host": "cts.example.com",
#             "is_admin": True,
#             "is_creator": True,
#             "locale": "en",
#             "manufacturer": None,
#             "platform": None,
#             "platform_package_id": None,
#             "user_huid": "f16cdc5f-6366-5552-9ecd-c36290ab3d11",
#             "username": None,
#         },
#         "proto_version": 4,
#     }
#
#     # - Act -
#     with TestClient(get_application()) as test_client:
#         response = test_client.post(
#             "/command",
#             json=payload,
#         )
#
#     # - Assert -
#     assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
#
#     status_message = response.json()["error_data"]["status_message"]
#     assert status_message == (
#         "No credentials for bot c755e147-30a5-45df-b46a-c75aa6089c8f"
#     )
