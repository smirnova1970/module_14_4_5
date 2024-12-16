"""The "Customer Registration" task:
Preparation:
To solve this task, you will need the code from the previous task. Complete it by following the task items below.

Complete the file crud_functions.py by writing and completing the following functions in it:
initiate_db, add the creation of the Users table, if it has not yet been created using an SQL query. This table should
contain the following fields:
id - integer, primary key
username - text (not empty)
email - text (not empty)
age - integer (not empty)
balance - integer (not empty)
add_user(username, email, age), which accepts: username, email address, and age. This function should add a record
with the transferred data to the Users table of your database. The balance of new users is always 1000. To add
records to the table, use an SQL query.
is_included(username) accepts the user name and returns True if such a user exists in the Users table, otherwise False.
To get the records, use an SQL query.

Changes in the Telegram bot:
Add the "Register" button to the main menu buttons.
Write a new RegistrationState state class with the following State class objects: username, email, age,
balance(default 1000).
Create a chain of RegistrationState state changes.
State chain functions RegistrationState:
sing_up(message):
Wrap it in a message_handler that responds to the text message 'Registration'.
This function should output the message "Enter the user name (Latin alphabet only) to the Telegram bot:".
After waiting for the name to be entered in the RegistrationState.username attribute using the set method.
set_username(message, state):
Wrap it in a message_handler that reacts to the state of RegistrationState.username.
If the message.text user is not yet in the table, then the data in the username state on message.text should
be updated. Next, the message "Enter your email:" is displayed and the new state of RegistrationState.email is accepted.
If a user with such a message.text is in the table, then output "The user exists, enter a different name" and request
a new state for RegistrationState.username.
set_email(message, state):
Wrap it in a message_handler that reacts to the state of RegistrationState.email.
This function should update the data in the RegistrationState.email status to message.text.
Next, display the message "Enter your age:":
After waiting for the age to be entered in the RegistrationState.age.
set_age(message, state) attribute:
Wrap it in a message_handler that reacts to the state of RegistrationState.age.
This function should update the data in the RegistrationState.age state to message.text.
Next, take all the data (username, email, and age) from the state and write it to the Users table using the
previously written crud function add_user.
At the end, complete the reception of states using the finish() method.
Before starting the bot, replenish your Products table with 4 or more entries for subsequent output in the
Telegram bot chat."""


# import logging
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from crud_function import *
#
# from pythonProject1.module_14.crud_functions import get_all_products
#
# logging.basicConfig(level=logging.INFO)
#
#
# api = ''
# bot = Bot(token=api)
# dp = Dispatcher(bot, storage=MemoryStorage())
#
# kb = ReplyKeyboardMarkup(
#     [
#         [
#             KeyboardButton(text='Рассчитать'),
#             KeyboardButton(text='Информация')
#         ],
#         [
#             KeyboardButton(text='Купить'),
#             KeyboardButton(text='Регистрация')
#         ]
#     ],
#     resize_keyboard=True
# )
#
# kb1 = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
#         InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
#     ]
# )
#
#
# kb2 = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
#          InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
#          InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
#          InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')]
#     ]
# )
#
# class UserState(StatesGroup):
#     age = State()
#     growth = State()
#     weight = State()
#
#
# class RegistrationState(StatesGroup):
#     username = State()
#     email = State()
#     age = State()
#     balance = 1000
#
#
# @dp.message_handler(text='Купить')
# async def get_buying_list(message: types.Message):
#     base = get_all_products()
#     for number in base:
#         await message.answer(f'Название:Продукт {number[1]} / Описание: описание {number[2]} / Цена: {number[3]}')
#         with open(f'{number[0]}.jpg', 'rb') as file:
#             await message.answer_photo(file)
#     await message.answer('Выберите продукт для покупки:', reply_markup=kb2)
#
#
# @dp.callback_query_handler(text='product_buying')
# async def send_confirm_message(call):
#     await call.message.answer('Вы успешно приобрели продукт!')
#     await call.answer()
#
#
# @dp.message_handler(text='Рассчитать')
# async def main_menu(message):
#     await message.answer('Выберите опцию:', reply_markup=kb1)
#
#
# @dp.callback_query_handler(text='formulas')
# async def get_formulas(call):
#     await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
#                               'Для женщин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161')
#     await call.answer()
#
#
# @dp.message_handler(commands=['start'])
# async def start(message):
#     await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup=kb)
#
#
# @dp.message_handler(text=['Информация'])
# async def main_menu(message: types.Message):
#     await message.answer('Выберите опцию:', reply_markup=kb1)
#
#
# @dp.message_handler()
# async def all_massages(message):
#     await message.answer('Нажмите /START, чтобы начать общение.')
#
#
# @dp.message_handler(commands=['start'])
# async def start(message):
#     await message.answer('Привет! Я бот помогающий твоему здоровью!\n\nНажмите /Рассчитать, чтобы посчитать '
#                          'необходимое вам суточное количество калорий', reply_markup=kb, parse_mode='HTML')
#
#
# @dp.message_handler(text='Информация')
# async def info(message):
#     await message.answer('Я - бот, который знает секрет как похудеть!')
#
#
# @dp.message_handler(text='Рассчитать')
# async def set_gender(message):
#     await message.answer('Введите свой пол (М/Ж):')
#     await UserState.gender.set()
#
# @dp.message_handler(text=['Регистрация'])
# async def sing_up(message: types.Message):
#     await message.answer('Введите имя пользователя (только латинский алфавит): ')
#     await RegistrationState.username.set()
#
# @dp.message_handler(state=RegistrationState.username)
# async def set_username(message: types.Message, state: FSMContext):
#     if is_included(message.text):
#         await message.answer('Пользователь существует, введите другое имя')
#         await RegistrationState.username.set()
#     else:
#         await state.update_data(username=message.text)
#         await message.answer('Введите свой email: ')
#         await RegistrationState.email.set()
#
# @dp.message_handler(state=RegistrationState.age)
# async def set_age(message: types.Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.update_data(balance=1000)
#     data = await state.get_data()
#     add_user(data['username'], data['email'], data['age'], data['balance'])
#     await message.answer("Регистрация прошла успешно")
#     await state.finish()
#
#
# @dp.message_handler(state=RegistrationState.email)
# async def set_email(message: types.Message, state: FSMContext):
#     await state.update_data(email=message.text)
#     await message.answer('Введите свой возраст: ')
#     await RegistrationState.age.set()
#
#
# @dp.message_handler(state=UserState.age)
# async def set_growth(message, state):
#     await state.update_data(age=int(message.text))
#     await message.answer('Введите свой рост:')
#     await UserState.growth.set()
#
#
# @dp.message_handler(state=UserState.growth)
# async def set_weight(message, state):
#     await state.update_data(growth=int(message.text))
#     await message.answer('Введите свой вес:')
#     await UserState.weight.set()
#
#
# @dp.message_handler(state=UserState.weight)
# async def send_calories(message, state):
#     await state.update_data(weight=int(message.text))
#     data = await state.get_data()
#     age = data['age']
#     growth = data['growth']
#     weight = data['weight']
#     gender = data['gender']
#     gender.lower()
#     if gender == 'м':
#         calories = 10 * weight + 6.25 * growth - 5 * age + 5
#     elif gender == 'ж':
#         calories = 10 * weight + 6.25 * growth - 5 * age - 161
#     else:
#         await message.answer('Вы ввели ошибочные данные')
#     await message.answer(f"Ваша норма калорий: {calories} ккал")
#     await state.finish()
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)



import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_function import *
from pythonProject1.module_14.crud_functions import get_all_products

logging.basicConfig(level=logging.INFO)

api = ''  # Замените на ваш токен
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Регистрация')
        ]
    ],
    resize_keyboard=True
)

kb1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
         InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')]
    ]
)


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    base = get_all_products()
    for number in base:
        await message.answer(f'Название: Продукт {number[1]} / Описание: описание {number[2]} / Цена: {number[3]}')
        with open(f'{number[0]}.jpg', 'rb') as file:
            await message.answer_photo(file)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await messa

ge.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        'Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
        'Для женщин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161'
    )
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.answer('Я - бот, который знает секрет как похудеть!')


@dp.message_handler(text='Рассчитать')
async def set_gender(message: types.Message):
    await message.answer('Введите свой пол (М/Ж):')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def get_gender(message: types.Message, state: FSMContext):
    gender = message.text.strip().lower()
    if gender in ['м', 'ж']:
        await state.update_data(gender=gender)
        await message.answer('Введите свой возраст:')
        await UserState.age.set()
    else:
        await message.answer('Ошибка! Введите "М" или "Ж".')


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    gender = data['gender']

    if gender == 'м':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    elif gender == 'ж':
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
    else:
        await message.answer('Вы ввели ошибочные данные')
        return  # Завершаем выполнение функции, если данные неверные

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал")
    await state.finish()


@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if is_included(message.text):  # Предполагается, что функция is_included определена
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email: ')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст: ')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])  # Предполагается, что функция add_user определена
    await message.answer("Регистрация прошла успешно")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

