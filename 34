import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton
import config
import crud_functions

crud_functions.initiate_db()
if crud_functions.products_is_empty():
    crud_functions.populate_products()
products = crud_functions.get_all_products()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')],
        [KeyboardButton(text='Регистрация')]
    ], resize_keyboard=True
)

calories_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий',
                                 callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта',
                                 callback_data='formulas')
        ]
    ]
)

goods_kb = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text='Product1',
                             callback_data='product_buying'),
        InlineKeyboardButton(text='Product2',
                             callback_data='product_buying'),
        InlineKeyboardButton(text='Product3',
                             callback_data='product_buying'),
        InlineKeyboardButton(text='Product4',
                             callback_data='product_buying')
    ]]
)


@dp.message_handler(text=['Рассчитать'])
async def send_inline_menu(message):
    await message.answer('Выберите опцию:', reply_markup=calories_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(
        '10·вес(кг) + 6.25·рост(см) – 5·возраст(лет) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст (лет):')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age=float(message.text))
    except ValueError:
        await message.answer('Введите свой возраст (лет):')
        await UserState.age.set()
    else:
        await message.answer('Введите свой рост (см):')
        await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth=float(message.text))
    except ValueError:
        await message.answer('Введите свой рост (см):')
        await UserState.growth.set()
    else:
        await message.answer('Введите свой вес (кг):')
        await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        await state.update_data(weight=float(message.text))
    except ValueError:
        await message.answer('Введите свой вес (кг):')
        await UserState.weight.set()
    else:
        data = await state.get_data()
        # Resting energy expenditure
        REE = 10 * data['weight'] \
            + 6.25 * data['growth'] \
            - 5 * data['age'] + 5
        await message.answer(
            f'Ваша суточная норма {round(REE, 2)} килокалорий')
        await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(
        'Привет! Я бот помогающий вашему здоровью.'
        ' Нажмите "Рассчитать", чтобы узнать вашу суточную норму'
        ' потребления килокалорий', reply_markup=start_kb)


@dp.message_handler(text=['Информация'])
async def info(message):
    await message.answer(
        'Данный бот подсчитывает норму потребления калорий для мужчин по'
        ' упрощённой формуле Миффлина - Сан Жеора'
        ' (https://www.calc.ru/Formula-Mifflinasan-Zheora.html).')


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for product in products:
        id, title, description, price = product
        await message.answer(f'Название: {title} | '
                             f'Описание: {description} | '
                             f'Цена: {price}')
        with open(f'product{id}.jpg', 'rb') as img:
            await message.answer_photo(img)

    await message.answer('Выберите продукт для покупки:',
                         reply_markup=goods_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler(text=['Регистрация'])
async def sign_up(message):
    await message.answer(
        'Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
        return
    await state.update_data(username=message.text)
    await message.answer('Введите свой email:')
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Пользователь {data["username"]} зарегистрирован.')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
