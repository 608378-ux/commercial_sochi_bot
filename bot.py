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
# КЛАВИАТУРЫ ОПРОСНИКА
# =========================

def deal_type_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Продажа", callback_data="deal_sale"),
        InlineKeyboardButton("Аренда", callback_data="deal_rent")
    )
    return kb


# =========================
# /start
# =========================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # deeplink из группы: ?start=post
    if message.get_args() == "post":
        await message.answer(
            "✍️ Размещение объявления\n\n"
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
        "Выберите тип сделки:",
        reply_markup=deal_type_kb()
    )
    await AdForm.type.set()

    @dp.callback_query_handler(lambda c: c.data in ["deal_sale", "deal_rent"], state=AdForm.type)
async def process_deal_type(callback: types.CallbackQuery, state: FSMContext):
    deal_type = "Продажа" if callback.data == "deal_sale" else "Аренда"

    await state.update_data(type=deal_type)
    await callback.answer()

    await callback.message.answer(
        f"Тип сделки: <b>{deal_type}</b>\n\n"
        "Укажите назначение объекта.",
        parse_mode="HTML"
    )



# =========================
# СВЯЗЬ С АДМИНИСТРАТОРОМ
# =========================

@dp.message_handler(lambda m: m.text == "Связаться с администратором")
async def contact_admin(message: types.Message):
    await message.answer(
        "📞 Контакты администратора:\n\n"
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
# ЗАПУСК
# =========================

# asyncio.get_event_loop().run_until_complete(send_post_button_once())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)





