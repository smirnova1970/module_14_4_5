"""Complete the previously written code for the Telegram bot:
Create a crud_functions file.py and write the following functions there:
initiate_db, which creates a Products table if it has not already been created using an SQL query.
This table should contain the following fields:
id - integer, primary key
title (product name) - text (not empty)
description(description) - text
price(price) - integer (not empty)
get_all_products, which returns all records from the Products table obtained using an SQL query.

Changes to the Telegram bot:
At the very beginning, run the previously written get_all_products function.
Change the get_buying_list function in the Telegram bot module, using the get_all_products function instead of
the usual product numbering. Use the received records in the output label: "Title: <title> |
Description: <description> | Price: <price>"
Before launching the bot, fill up your Products table with 4 or more entries for subsequent output in the
Telegram bot chat."""

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_function import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kl = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
kl.add(button)
kl.add(button2)

kb = InlineKeyboardMarkup(resize_keyboard=True)
button_ = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb.insert(button_)
kb.insert(button_2)
kb.insert(button_3)
kb.insert(button_4)

kp = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kp.insert(button)
kp.insert(button2)
kp.insert(button3)

initiate_db()
check_and_populate_products()
products = get_all_products()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    base = get_all_products()
    for number in base:
        await message.answer(f'Название:Продукт {number[1]} / Описание: описание {number[2]} / Цена: {number[3]}')
        with open(f'{number[0]}.jpg', 'rb') as file:
            await message.answer_photo(file)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kl)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
                              'Для женщин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup=kp)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Привет, я бот помогающий твоему здоровью!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Нажмите /START, чтобы начать общение.')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!\n\nНажмите /Рассчитать, чтобы посчитать '
                         'необходимое вам суточное количество калорий', reply_markup=kb, parse_mode='HTML')


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я - бот, который знает секрет как похудеть!')


@dp.message_handler(text='Рассчитать')
async def set_gender(message):
    await message.answer('Введите свой пол (М/Ж):')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    gender = data['gender']
    gender.lower()
    if gender == 'м':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    elif gender == 'ж':
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
    else:
        await message.answer('Вы ввели ошибочные данные')
    await message.answer(f"Ваша норма калорий: {calories} ккал")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
