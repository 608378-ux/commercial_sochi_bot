import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Нижнее меню (постоянные кнопки)
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add("АРЕНДА")
keyboard.add("ПРОДАЖА")

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Выберите раздел:",
        reply_markup=keyboard
    )

@dp.message_handler(lambda message: message.text == "АРЕНДА")
async def rent(message: types.Message):
    button = types.InlineKeyboardButton(
        text="Перейти к аренде",
        url="https://t.me/commercial_sochi?search=%23аренда"
    )
    inline_kb = types.InlineKeyboardMarkup().add(button)

    await message.answer(
        "Объявления по аренде:",
        reply_markup=inline_kb
    )

@dp.message_handler(lambda message: message.text == "ПРОДАЖА")
async def sale(message: types.Message):
    button = types.InlineKeyboardButton(
        text="Перейти к продаже",
        url="https://t.me/commercial_sochi?search=%23продажа"
    )
    inline_kb = types.InlineKeyboardMarkup().add(button)

    await message.answer(
        "Объявления по продаже:",
        reply_markup=inline_kb
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
