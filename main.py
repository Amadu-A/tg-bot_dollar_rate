import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import BOT_TOKEN

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()


def get_dollar_rate():
    """Функция для получения курса доллара"""
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    return data['Valute']['USD']['Value']


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Хэндлер на команду /start"""
    await state.set_state(Form.name)
    await message.answer("Добрый день. Как вас зовут?")


@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    """Хэндлер на все сообщения"""
    name = message.text
    dollar_rate = get_dollar_rate()
    response_message = f'Рад знакомству, {name}! Курс доллара сегодня {dollar_rate}р.'
    await state.update_data(name=message.text)
    await state.set_state(Form.like_bots)
    await message.answer(text=response_message)


async def main():
    """Запуск процесса поллинга новых апдейтов"""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())