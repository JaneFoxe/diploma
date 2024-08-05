import pytest
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock, Mock

from tg_bot.tg_bot import (
    start_handler,
    level_selection,
    select_topic,
    find_task,
    navigator_task,
    back_find_topic,
    update_list_task_topic,
    update_list_task,
    DateTask,
    Gen,
)


@pytest.fixture
def mock_message():
    message = Mock(spec=Message)
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_callback_query(mock_message):
    callback_query = Mock(spec=CallbackQuery)
    callback_query.message = mock_message
    callback_query.answer = AsyncMock()
    return callback_query


@pytest.fixture
def mock_state():
    state = Mock(spec=FSMContext)
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.get_data = AsyncMock(return_value={"topic": {"text": "mock_topic"}})
    return state


@pytest.fixture
def mock_callback_data():
    callback_data = Mock()
    callback_data.value = 0
    callback_data.text = "mock_text"
    return callback_data


@pytest.mark.asyncio
async def test_start_handler(mock_message, mock_state):
    mock_message.answer = AsyncMock()
    await start_handler(mock_message, mock_state)
    mock_message.answer.assert_called_once()
    mock_state.set_state.assert_called_once_with(Gen.level)


@pytest.mark.asyncio
async def test_level_selection(mock_callback_query, mock_callback_data, mock_state):
    mock_callback_query.answer = AsyncMock()
    mock_callback_query.message.answer = AsyncMock()
    DateTask.task_level = 0
    await level_selection(mock_callback_query, mock_callback_data, mock_state)
    mock_callback_query.answer.assert_called_once()
    mock_callback_query.message.answer.assert_called()
    mock_state.update_data.assert_called_once()
    mock_state.set_state.assert_called_once_with(Gen.topic)


@pytest.mark.asyncio
async def test_select_topic(mock_callback_query, mock_callback_data, mock_state):
    mock_callback_query.message.answer = AsyncMock()
    mock_state.update_data = AsyncMock()
    mock_state.get_data = AsyncMock(return_value={"topic": mock_callback_data})
    await select_topic(mock_callback_query, mock_callback_data, mock_state)
    mock_state.update_data.assert_called_once()
    mock_state.set_state.assert_called_once_with(Gen.task)
    mock_callback_query.message.answer.assert_called()


@pytest.mark.asyncio
async def test_find_task(mock_callback_query):
    mock_callback_query.message.answer = AsyncMock()
    await find_task(mock_callback_query)
    mock_callback_query.message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_navigator_task(mock_callback_query, mock_callback_data, mock_state):
    mock_callback_query.message.answer = AsyncMock()
    mock_state.get_data = AsyncMock(return_value={"topic": mock_callback_data})
    await navigator_task(mock_callback_query, mock_callback_data, mock_state)
    mock_callback_query.message.answer.assert_called()
    mock_state.get_data.assert_called_once()


@pytest.mark.asyncio
async def test_back_find_topic(mock_callback_query, mock_state):
    mock_callback_query.message.answer = AsyncMock()
    await back_find_topic(mock_callback_query, mock_state)
    mock_callback_query.message.answer.assert_called_once()
    mock_state.set_state.assert_called_once_with(Gen.topic)
