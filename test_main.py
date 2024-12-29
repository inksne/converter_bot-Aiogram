from aiogram import types
from aiogram.enums.chat_action import ChatAction
from aiogram.utils.markdown import hbold
from unittest.mock import AsyncMock

import pytest

from main import handle_start, handle_comands, handle_image_to_ico


async def echo(message: types.Message):
    await message.answer(message.text)


@pytest.mark.asyncio
async def test_echo_handler():
    text_mock = "test123"
    message_mock = AsyncMock(text=text_mock)
    await echo(message=message_mock)
    message_mock.answer.assert_called_with(text_mock)


@pytest.mark.asyncio
async def test_handle_start():
    message_mock = AsyncMock(text='/start', from_user=types.User(
        id=123,
        first_name="Test",
        last_name="User",
        username="testuser",
        is_bot=False
    ))
    await handle_start(message=message_mock)
    message_mock.answer.assert_called_once()

    assert "Приветствую" in message_mock.answer.call_args[1]['text']


@pytest.mark.asyncio
async def test_handle_comands():
    mock_message = AsyncMock()
    mock_message.chat = AsyncMock(id=123)
    mock_message.bot = AsyncMock()

    await handle_comands(mock_message)

    mock_message.bot.send_chat_action.assert_called_once_with(
        chat_id=mock_message.chat.id, action=ChatAction.TYPING
    )
    mock_message.answer.assert_called_once()
    text = mock_message.answer.call_args[1]['text']

    assert hbold("Список всех команд:") in text


@pytest.mark.asyncio
async def test_handle_image_to_ico_no_photo():
    mock_message = AsyncMock()
    mock_message.photo = None

    await handle_image_to_ico(mock_message)

    mock_message.answer.assert_called_once_with("Пожалуйста, отправьте изображение с командой /image_to_ico.")