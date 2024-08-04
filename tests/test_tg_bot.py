import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from magic_filter import F

from func import db_manager
from tg_bot.tg_bot import DateTask, NumbersCallbackFactory, Gen, get_task, router


@pytest.fixture
def mock_db_manager():
    mock_db = MagicMock()
    db_manager.DBManager = MagicMock(return_value=mock_db)
    DateTask.db = mock_db
    return mock_db


@pytest.fixture
def mock_state():
    return AsyncMock(FSMContext)


@pytest.mark.asyncio
async def test_start_handler(mock_state):
    message = AsyncMock(Message)
    message.answer = AsyncMock()

    await router.message[Command("start")].handler(message, mock_state)

    message.answer.assert_called_with(
        "Привет! Выберите уровень сложности, чтобы начать решать задачи",
        reply_markup=get_keyboard_fab(),
    )
    mock_state.set_state.assert_called_with(Gen.level)


@pytest.mark.asyncio
async def test_level_selection(mock_db_manager, mock_state):
    callback_query = AsyncMock(CallbackQuery)
    callback_data = NumbersCallbackFactory(
        action="level", value=1, text="Обычные задачи"
    )
    callback_query.message.answer = AsyncMock()
    callback_query.answer = AsyncMock()

    await router.callback_query[
        Gen.level, NumbersCallbackFactory.filter(F.action == "level")
    ].handler(callback_query, callback_data, mock_state)

    assert DateTask.task_level == 1
    mock_state.update_data.assert_called_with(level=callback_data)
    mock_state.set_state.assert_called_with(Gen.topic)
    callback_query.answer.assert_called_with(text="Выбран уровень: Обычные задачи ")
    callback_query.message.answer.assert_called_with("Уровень: Обычные задачи ")
    callback_query.message.answer.assert_called_with(
        "По какой категории будем смотреть задачи", reply_markup=get_keyboard_topic()
    )


@pytest.mark.asyncio
async def test_select_topic(mock_db_manager, mock_state):
    callback_query = AsyncMock(CallbackQuery)
    callback_data = NumbersCallbackFactory(action="task_topic", value=0, text="math")
    callback_query.message.answer = AsyncMock()
    callback_query.answer = AsyncMock()

    await router.callback_query[
        Gen.topic, NumbersCallbackFactory.filter(F.action == "task_topic")
    ].handler(callback_query, callback_data, mock_state)

    assert DateTask.topic == "math"
    mock_state.update_data.assert_called_with(topic=callback_data)
    mock_state.set_state.assert_called_with(Gen.task)

    callback_query.message.answer.assert_called_with(
        "  --- задачи из категории math --- ", parse_mode="HTML"
    )
    callback_query.message.answer.assert_called_with(get_task(), parse_mode="HTML")


@pytest.mark.asyncio
async def test_find_task(mock_db_manager, mock_state):
    message = AsyncMock(Message)
    message.answer = AsyncMock()

    await router.callback_query[
        Gen.task, NumbersCallbackFactory.filter(F.action == "find_task")
    ].handler(message)

    message.answer.assert_called_with("Уточните какую задачу искать")


@pytest.mark.asyncio
async def test_navigator_task(mock_db_manager, mock_state):
    callback_query = AsyncMock(CallbackQuery)
    callback_data = NumbersCallbackFactory(action="navigator_task", value=1, text="+1")
    callback_query.message.answer = AsyncMock()
    mock_state.get_data = AsyncMock(
        return_value={
            "topic": NumbersCallbackFactory(action="task_topic", value=0, text="math")
        }
    )

    await router.callback_query[
        Gen.task, NumbersCallbackFactory.filter(F.action == "navigator_task")
    ].handler(callback_query, callback_data, mock_state)

    assert DateTask.task_page == 1
    callback_query.message.answer.assert_called_with(get_task(), parse_mode="HTML")
    callback_query.message.answer.assert_called_with(
        "  --- страница 1 --- списка задач по #math#", reply_markup=get_keyboard_task()
    )
