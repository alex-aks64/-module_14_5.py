from mailbox import Message
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import texts
from keybords import *
from crud_functions import *
from registr import *



APM="_v3q9jzE5lDgT6KPpL5js0I"
bot=Bot(token=APM)
dp=Dispatcher(bot,storage= MemoryStorage())



@dp.message_handler(text=['start','/start'])
async def start(message):
    print(f'Мы получили собщение {message.text} ')
    with open('1.jpg',"rb") as j:
        await message.answer_photo(j,texts.b,reply_markup=kb)



@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    producs=get_all_products()
    for title in producs:
        product_info = f'Название: {title[1]} | Описание:  {title[2]} | Цена: {title[3]}'
        await message.answer(product_info)
        with open(f'im/{title[1]}.jpg', "rb") as j:
            await message.answer_photo(j)
    await message.answer(texts.b2,reply_markup=ikb)



@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
        await call.message.answer(texts.b3)
        await call.answer()




class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class  RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()
    

@dp.message_handler(text=['Информация','/info'])
async def info(message):
    await message.answer('Информация о боте:')
    await message.answer('Команда /start - начало работы с ботом')
    await message.answer('Команда /info - получение информации о боте')
    await message.answer('Команда /calories - начало рассчета калорий')



@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
        await message.answer(f'Введите ваш возраст:')
        await UserState.age.set()




@dp.message_handler(state=UserState.age)
async def set_growth(message,state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите ваш рост:')
    print(f'мы сохранили {message.text}')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите ваш вес:')
    print(f'мы сохранили {message.text}')
    await UserState.weight.set()



@dp.message_handler(state=UserState.weight)
async def send_calories(message,state):
    print(f'мы сохранили {message.text}')
    await state.update_data(weight=float(message.text))
    data= await state.get_data()
    # Simplified Mifflin - St Jeor formula for calorie calculation (example for women)
    calories = 655 + (9.6 * data['weight']) + (1.8 * data['growth']) - (4.7 * data['age'])
    await message.answer(f'Ваша максимальная норма калорий: {calories}')
    await state.finish()
    
# Регистрация стек

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state = RegistrationState.username)
async def set_username(message,state):
        if is_included(message.text):
            await message.answer("Пользователь существует, введите другое имя")
            await RegistrationState.username.set()
        else:
            await state.update_data(username=message.text)
            await message.answer("Введите свой email (формат: 123@example.com):")
            await RegistrationState.email.set()


@dp.message_handler(state= RegistrationState.email)
async def set_email(message,state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()



@dp.message_handler(state= RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    users_data= await state.get_data()
    add_user(username=users_data["username"],email=users_data["email"],age=int(users_data["age"]))
    await state.finish()
    await message.answer(f'Увожаемый пользователь {message.from_user.username}\n Регистрация прошла успешна.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)