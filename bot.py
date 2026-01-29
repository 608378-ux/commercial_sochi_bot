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
    # deeplink из группы: ?start=post
    if message.get_args() == "post":
        await message.answer(
            "Размещение объявления\n\n"
            "Пожалуйста, ответьте на несколько вопросов.",
            reply_markup=keyboard
        )
        await AdForm.type.set()
        return

    # обычный запуск бота
    await message.answer(
        "Добро пожаловать!\nВыберите действие:",
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
        "Опишите объект:\nплощадь, район, этаж, цена \nдобавьте описание"
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
        "Контакты администратора:\n\n"
        "Телефон: +7 938 400-05-58\n"
        "Telegram: https://t.me/Svetla_Sochi\n"
       
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
# КНОПКИ В ТЕМЕ "РАЗМЕСТИТЬ ОБЪЯВЛЕНИЕ"
# =========================

@dp.message_handler(commands=["post"])
async def post_entry(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    btn_post = types.InlineKeyboardButton(
        text="Разместить объявление",
        callback_data="post_stub"
    )

    btn_contact = types.InlineKeyboardButton(
        text="Связаться с администратором",
        callback_data="contact_admin"
    )

    keyboard.add(btn_post, btn_contact)

    await message.answer(
        "Выберите действие:",
        reply_markup=keyboard
    )

# =========================
# Обработчики ЗАГЛУШКИ и связи с админом
# =========================

@dp.callback_query_handler(lambda c: c.data == "post_stub")
async def post_stub(callback_query: types.CallbackQuery):
    await callback_query.answer()

    await callback_query.message.answer(
        "Размещение объявления скоро будет доступно.\n\n"
        "Пока вы можете связаться с администратором для публикации."
    )


@dp.callback_query_handler(lambda c: c.data == "contact_admin")
async def contact_admin(callback_query: types.CallbackQuery):
    await callback_query.answer()

    await callback_query.message.answer(
        "Контакты администратора:\n\n"
        "Телефон: +7 938 400-05-58\n"
        "Telegram: https://t.me/Svetla_Sochi"
    )

import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

GROUP_ID = -1003844187449   # ✅ твой chat_id
TOPIC_ID = 24              # тема "Разместить объявление"

async def send_post_button_once():
    bot = Bot(token=API_TOKEN, parse_mode="HTML")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Разместить объявление",
                    url="https://t.me/commercial_sochi_bot?start=post"
                )
            ]
        ]
    )

    text = (
        "<b>РАЗМЕСТИТЬ ОБЪЯВЛЕНИЕ</b>\n\n"
        "В этой базе публикуются только проверенные объявления "
        "о коммерческой недвижимости в Сочи.\n\n"
        "Чтобы разместить объект:\n\n"
        "1️⃣ Нажмите кнопку «Разместить объявление»\n"
        "2️⃣ Заполните короткую форму\n"
        "3️⃣ Объявление пройдёт модерацию\n\n"
        "⛔️ Публикация объявлений напрямую в группе закрыта"
    )

    await bot.send_message(
        chat_id=GROUP_ID,
        message_thread_id=TOPIC_ID,
        text=text,
        reply_markup=keyboard
    )

    await bot.session.close()



# =========================
# ЗАПУСК
# =========================

asyncio.get_event_loop().run_until_complete(send_post_button_once())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

