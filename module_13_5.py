from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "----------------------------------------------"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
Button_1 = KeyboardButton(text="Рассчитать")
Button_2 = KeyboardButton(text="Информация")
kb.row(Button_1, Button_2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Расчёт индивидуальной калорийности продуктов:", reply_markup=kb)


@dp.message_handler(text=["Рассчитать"])
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_caloris(message, state):
    await state.update_data(weight_=message.text)
    data = await state.get_data()
    calorie_norms = (10.0 * float(data['weight_']) +
                     6.25 * float(data['growth_']) -
                     5.0 * float(data['age_']) + 5.0) * 1.2
    await message.answer(f'Ваша норма калорийности питания: \n\t\t{calorie_norms} ккал/день')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
