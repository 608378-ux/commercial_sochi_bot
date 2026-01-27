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

# ===== АРЕНДА =====

async def send_rent(message: types.Message):
    button = types.InlineKeyboardButton(
        text="Перейти к аренде",
        url="https://t.me/commercial_sochi?search=%23аренда"
    )
    inline_kb = types.InlineKeyboardMarkup().add(button)

    await message.answer(
        "Объявления по аренде:",
        reply_markup=inline_kb
    )


@dp.message_handler(commands=["rent"])
async def rent_command(message: types.Message):
    await send_rent(message)


@dp.message_handler(lambda message: message.text == "АРЕНДА")
async def rent_button(message: types.Message):
    await send_rent(message)


# ===== ПРОДАЖА =====

async def send_sale(message: types.Message):
    button = types.InlineKeyboardButton(
        text="Перейти к продаже",
        url="https://t.me/commercial_sochi?search=%23продажа"
    )
    inline_kb = types.InlineKeyboardMarkup().add(button)

    await message.answer(
        "Объявления по продаже:",
        reply_markup=inline_kb
    )


@dp.message_handler(commands=["sale"])
async def sale_command(message: types.Message):
    await send_sale(message)


@dp.message_handler(lambda message: message.text == "ПРОДАЖА")
async def sale_button(message: types.Message):
    await send_sale(message)

# --- НАВИГАЦИЯ В КАНАЛЕ (добавка, не ломает бота) ---

@dp.message_handler(commands=["channel_menu"])
async def channel_menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        types.InlineKeyboardButton(
            text="Аренда коммерческой",
            url="https://t.me/commercial_sochi?search=%23аренда"
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text="Продажа коммерческой",
            url="https://t.me/commercial_sochi?search=%23продажа"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="Открыть бот",
            url="https://t.me/commercial_sochi_bot"
        )
    )

    await bot.send_message(
        chat_id="@commercial_sochi",
        text="Навигация по каналу\n\nВыберите раздел:",
        reply_markup=keyboard
    )

    await message.answer("Навигация для канала отправлена.")

    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

