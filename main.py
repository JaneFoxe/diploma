import os
import subprocess
import sys

import schedule
from dotenv import load_dotenv
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from func.problem_parser import parsing_code
from tg_bot.tg_bot import router


load_dotenv(".env")


async def main():
    bot = Bot(token=os.getenv("BOT_TG_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    # запуск бота
    logging.basicConfig(level=logging.INFO)
    # Запуск скрипта инициализации базы данных
    subprocess.run([sys.executable, "func/initialize_db.py"], check=True)

    asyncio.run(main())
    # запуск расписания
    schedule.every().hour.run(parsing_code())
