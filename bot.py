import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# =========================
# НИЖНЕЕ МЕНЮ
# =========================

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add("Разместить объявление")
keyboard.add("Связаться с администратором")
keyboard.add("ПРОДАЖА смотреть объявления")
keyboard.add("АРЕНДА смотреть объявления")


# =========================
# FSM — ОПРОСНИК
# =========================

class AdForm(StatesGroup):
    type = State()
    description = State()
    contact = State()


# =========================
# /start
# =========================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать 👋\nВыберите действие:",
        reply_markup=keyboard
    )


# =========================
# РАЗМЕСТИТЬ ОБЪЯВЛЕНИЕ
# =========================

@dp.message_handler(lambda m: m.text == "Разместить объявление")
async def add_ad_start(message: types.Message):
    await message.answer(
        "Что вы размещаете?\nНапишите: Аренда или Продажа"
    )
    await AdForm.type.set()


@dp.message_handler(state=AdForm.type)
async def add_ad_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer(
        "Опишите объект:\nплощадь, район, этаж, цена"
    )
    await AdForm.description.set()


@dp.message_handler(state=AdForm.description)
async def add_ad_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        "Оставьте контакт для связи (телефон или Telegram)"
    )
    await AdForm.contact.set()


@dp.message_handler(state=AdForm.contact)
async def add_ad_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()

    text = (
        "✅ Заявка на размещение получена\n\n"
        f"Тип: {data['type']}\n"
        f"Описание: {data['description']}\n"
        f"Контакт: {message.text}\n\n"
        "Администратор свяжется с вами."
    )

    await message.answer(text, reply_markup=keyboard)
    await state.finish()


# =========================
# СВЯЗЬ С АДМИНИСТРАТОРОМ
# =========================

@dp.message_handler(lambda m: m.text == "Связаться с администратором")
async def contact_admin(message: types.Message):
    await message.answer(
        "📞 Контакты администратора:\n\n"
        "Телефон: +7 9XX XXX-XX-XX\n"
        "Telegram: https://t.me/username\n"
        "Канал администратора: https://t.me/sochi_commerc"
    )


# =========================
# ПРОДАЖА
# =========================

@dp.message_handler(lambda m: m.text == "ПРОДАЖА смотреть объявления")
async def sale(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="Открыть объявления о продаже",
            url="https://t.me/sochi_commerc/4"
        )
    )
    await message.answer("Продажа коммерческой недвижимости:", reply_markup=kb)


# =========================
# АРЕНДА
# =========================

@dp.message_handler(lambda m: m.text == "АРЕНДА смотреть объявления")
async def rent(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="Открыть объявления об аренде",
            url="https://t.me/sochi_commerc/3"
        )
    )
    await message.answer("Аренда коммерческой недвижимости:", reply_markup=kb)


# =========================
# ЗАПУСК
# =========================

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

