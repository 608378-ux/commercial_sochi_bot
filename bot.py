import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv("BOT_TOKEN")

MODERATION_CHAT_ID = -5135426236

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


photos_done_kb = ReplyKeyboardMarkup(
    resize_keyboard=True
)
photos_done_kb.add("Готово")



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
    deal_type = State()
    purpose = State()
    area = State()
    district = State()
    address = State()
    description = State()
    photos = State()
    price = State()
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
# КЛАВИАТУРА Назначение объекта
# =========================

def purpose_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Свободного назначения", callback_data="purpose_free"),
        InlineKeyboardButton("Торговая площадь", callback_data="purpose_trade"),
        InlineKeyboardButton("Офисная недвижимость", callback_data="purpose_office"),
        InlineKeyboardButton("Гостиничная недвижимость", callback_data="purpose_hotel"),
        InlineKeyboardButton("Склады", callback_data="purpose_warehouse"),
        InlineKeyboardButton("Производственные помещения", callback_data="purpose_industrial"),
        InlineKeyboardButton("Другое", callback_data="purpose_other"),
    )
    return kb

# =========================
# КЛАВИАТУРА Район
# =========================

def district_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Адлерский", callback_data="district_adler"),
        InlineKeyboardButton("Хостинский", callback_data="district_khosta"),
        InlineKeyboardButton("Лазаревский", callback_data="district_lazarev"),
        InlineKeyboardButton("Центральный", callback_data="district_center"),
        InlineKeyboardButton("Сириус", callback_data="district_sirius"),
        InlineKeyboardButton("Красная Поляна", callback_data="district_polana"),
    )
    return kb



def edit_menu_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Тип сделки", callback_data="edit_type"),
        InlineKeyboardButton("Назначение", callback_data="edit_purpose"),
        InlineKeyboardButton("Площадь", callback_data="edit_area"),
        InlineKeyboardButton("Район", callback_data="edit_district"),
        InlineKeyboardButton("Адрес", callback_data="edit_address"),
        InlineKeyboardButton("Описание", callback_data="edit_description"),
        InlineKeyboardButton("Цена", callback_data="edit_price"),
        InlineKeyboardButton("📸 Фото", callback_data="edit_photos"),
    )
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="edit_back")
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
        await AdForm.deal_type.set()
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
    await AdForm.deal_type.set()


@dp.callback_query_handler(
    lambda c: c.data in ["deal_sale", "deal_rent"],
    state=AdForm.deal_type
)
async def process_deal_type(callback: types.CallbackQuery, state: FSMContext):
    deal_type = "Продажа" if callback.data == "deal_sale" else "Аренда"

    await state.update_data(type=deal_type)
    await callback.answer()

    await callback.message.answer(
        f"Тип сделки: <b>{deal_type}</b>\n\n"
        "Выберите назначение объекта:",
        reply_markup=purpose_kb(),
        parse_mode="HTML"
    )

    await AdForm.purpose.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith("purpose_"),
    state=AdForm.purpose
)
async def process_purpose(callback: types.CallbackQuery, state: FSMContext):
    mapping = {
        "purpose_free": "Свободного назначения",
        "purpose_trade": "Торговая площадь",
        "purpose_office": "Офисная недвижимость",
        "purpose_hotel": "Гостиничная недвижимость",
        "purpose_warehouse": "Склады",
        "purpose_industrial": "Производственные помещения",
        "purpose_other": "Другое",
    }

    purpose = mapping.get(callback.data)

    await state.update_data(purpose=purpose)
    await callback.answer()

    await callback.message.answer(
        f"Назначение: <b>{purpose}</b>\n\n"
        "Укажите площадь объекта (в м²):",
        parse_mode="HTML"
    )

    await AdForm.area.set()



@dp.message_handler(state=AdForm.area)
async def process_area(message: types.Message, state: FSMContext):
    area_text = message.text.replace(",", ".")

    try:
        area = float(area_text)
        if area <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❗ Пожалуйста, введите площадь числом (например: 120)")
        return

    await state.update_data(area=area)

    await message.answer(
        f"Площадь: <b>{area} м²</b>\n\n"
        "Выберите район:",
        reply_markup=district_kb(),
        parse_mode="HTML"
    )

    await AdForm.district.set()



@dp.callback_query_handler(
    lambda c: c.data.startswith("district_"),
    state=AdForm.district
)
async def process_district(callback: types.CallbackQuery, state: FSMContext):
    mapping = {
        "district_adler": "Адлерский",
        "district_khosta": "Хостинский",
        "district_lazarev": "Лазаревский",
        "district_center": "Центральный",
        "district_sirius": "Сириус",
        "district_polana": "Красная Поляна",
    }

    district = mapping.get(callback.data)

    await state.update_data(district=district)
    await callback.answer()

    await callback.message.answer(
        f"Район: <b>{district}</b>\n\n"
        "Укажите адрес объекта:",
        parse_mode="HTML"
    )

    await AdForm.address.set()


@dp.message_handler(state=AdForm.address)
async def process_address(message: types.Message, state: FSMContext):
    address = message.text.strip()

    if len(address) < 5:
        await message.answer("❗ Пожалуйста, укажите корректный адрес.")
        return

    await state.update_data(address=address)

    await message.answer(
        "Введите описание объекта (до 500 символов):\n\n"
        "ℹ️ Можно указать:\n"
        "— состояние\n"
        "— планировку\n"
        "— особенности объекта"
    )

    await AdForm.description.set()


@dp.message_handler(state=AdForm.description)
async def process_description(message: types.Message, state: FSMContext):
    description = message.text.strip()

    if len(description) > 500:
        await message.answer(
            f"❗ Слишком длинное описание ({len(description)} символов)."
        )
        return

    await state.update_data(description=description)
    await state.update_data(photos=[])

    await message.answer(
        "📸 Добавьте фото объекта (до 10 шт).\n"
        "Когда закончите — нажмите «Готово».",
        reply_markup=photos_done_kb
    )

    await AdForm.photos.set()




@dp.message_handler(content_types=types.ContentType.PHOTO, state=AdForm.photos)
async def process_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    if len(photos) >= 10:
        await message.answer("⛔️ Можно добавить не более 10 фото.")
        return

    photo_id = message.photo[-1].file_id
    photos.append(photo_id)

    await state.update_data(photos=photos)

    await message.answer(f" Фото добавлено ({len(photos)}/10)")



@dp.message_handler(lambda m: m.text == "Готово", state=AdForm.photos)
async def photos_done(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if not data.get("photos"):
        await message.answer("❗ Добавьте хотя бы одно фото.")
        return

    await message.answer(
        "Введите цену объекта :\n\n",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await AdForm.price.set()




@dp.message_handler(state=AdForm.price)
async def process_price(message: types.Message, state: FSMContext):
    price = message.text.strip()

    if len(price) < 2:
        await message.answer("❗ Пожалуйста, укажите корректную цену.")
        return

    await state.update_data(price=price)

    # клавиатура контакта
    contact_kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    contact_kb.add(
        types.KeyboardButton("📞 Поделиться номером", request_contact=True)
    )
    contact_kb.add("✍️ Ввести вручную")

    await message.answer(
        "Укажите контакт для связи:",
        reply_markup=contact_kb
    )

    await AdForm.contact.set()



@dp.message_handler(content_types=types.ContentType.CONTACT, state=AdForm.contact)
async def process_contact_share(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    await finalize_ad(message, state, contact)


@dp.message_handler(state=AdForm.contact)
async def process_contact_manual(message: types.Message, state: FSMContext):
    contact = message.text.strip()

    if len(contact) < 5:
        await message.answer("❗ Укажите корректный контакт.")
        return

    await finalize_ad(message, state, contact)



async def finalize_ad(message: types.Message, state: FSMContext, contact: str):
    data = await state.get_data()

    text = (
        "📋 <b>Проверьте данные объявления:</b>\n\n"
        f"🔹 Тип сделки: {data['type']}\n"
        f"🔹 Назначение: {data['purpose']}\n"
        f"🔹 Площадь: {data['area']} м²\n"
        f"🔹 Район: {data['district']}\n"
        f"🔹 Адрес: {data['address']}\n"
        f"🔹 Цена: {data['price']}\n\n"
        f"📝 Описание:\n{data['description']}\n\n"
        f"📞 Контакт: {contact}"
    )

    confirm_kb = InlineKeyboardMarkup()
    confirm_kb.add(
        InlineKeyboardButton("✅ Отправить на модерацию", callback_data="send_moderation"),
        InlineKeyboardButton("✏️ Исправить", callback_data="edit_ad")
    )

    await state.update_data(contact=contact)

    await message.answer(
        text,
        reply_markup=confirm_kb,
        parse_mode="HTML"
    )



@dp.callback_query_handler(lambda c: c.data == "edit_ad", state="*")
async def edit_ad(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "✏️ Что вы хотите исправить?",
        reply_markup=edit_menu_kb()
    )





@dp.callback_query_handler(lambda c: c.data == "send_moderation", state="*")
async def send_to_moderation(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    text = (
        "🆕 <b>НОВОЕ ОБЪЯВЛЕНИЕ НА МОДЕРАЦИЮ</b>\n\n"
        f"🔹 Тип сделки: {data['type']}\n"
        f"🔹 Назначение: {data['purpose']}\n"
        f"🔹 Площадь: {data['area']} м²\n"
        f"🔹 Район: {data['district']}\n"
        f"🔹 Адрес: {data['address']}\n"
        f"🔹 Цена: {data['price']}\n\n"
        f"📝 Описание:\n{data['description']}\n\n"
        f"📞 Контакт: {data['contact']}"
    )

    moderation_kb = InlineKeyboardMarkup()
    moderation_kb.add(
        InlineKeyboardButton("✅ Одобрить", callback_data="approve_ad"),
        InlineKeyboardButton("❌ Отклонить", callback_data="reject_ad")
    )

    photos = data.get("photos", [])

    # отправляем первое фото с текстом
    if photos:
        await bot.send_photo(
            chat_id=MODERATION_CHAT_ID,
            photo=photos[0],
            caption=text,
            reply_markup=moderation_kb,
            parse_mode="HTML"
        )

        # остальные фото — без текста
        for photo_id in photos[1:]:
            await bot.send_photo(
                chat_id=MODERATION_CHAT_ID,
                photo=photo_id
            )
    else:
        await bot.send_message(
            chat_id=MODERATION_CHAT_ID,
            text=text,
            reply_markup=moderation_kb,
            parse_mode="HTML"
        )

    await callback.answer("Объявление отправлено на модерацию ✅")
    await callback.message.answer(
        "Спасибо! Ваше объявление отправлено на модерацию.\n"
        "Мы свяжемся с вами после проверки."
    )

    await state.finish()



@dp.callback_query_handler(lambda c: c.data == "approve_ad", state="*")
async def approve_ad(callback: types.CallbackQuery):
    await callback.answer("Объявление одобрено")
    await callback.message.reply("✅ Объявление одобрено")

@dp.callback_query_handler(lambda c: c.data == "reject_ad", state="*")
async def reject_ad(callback: types.CallbackQuery):
    await callback.answer("Объявление отклонено")
    await callback.message.reply("❌ Объявление отклонено")



@dp.callback_query_handler(lambda c: c.data == "edit_ad", state="*")
async def edit_ad(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "✏️ Что вы хотите исправить?\n\n"
        "Пока можно начать заново.",
        reply_markup=keyboard
    )
    await state.finish()



@dp.callback_query_handler(lambda c: c.data.startswith("edit_"))
async def choose_edit_field(callback: types.CallbackQuery, state: FSMContext):
    field = callback.data.replace("edit_", "")

    if field == "back":
        await callback.answer()
        await show_preview(callback.message, state)
        return

    await state.update_data(edit_field=field)
    await callback.answer()

    prompts = {
        "type": "Введите новый тип сделки (Продажа / Аренда):",
        "purpose": "Введите новое назначение:",
        "area": "Введите новую площадь:",
        "district": "Введите новый район:",
        "address": "Введите новый адрес:",
        "description": "Введите новое описание:",
        "price": "Введите новую цену:",
        "photos": "Отправьте новые фото (старые будут удалены).",
    }

    await callback.message.answer(prompts.get(field, "Введите новое значение:"))



@dp.message_handler(state="*")
async def process_edit_value(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if "edit_field" not in data:
        return

    field = data["edit_field"]

    # фото отдельно
    if field == "photos":
        await state.update_data(photos=[])
        await message.answer("📸 Отправьте фото заново (до 10 шт), затем напишите «Готово»")
        await state.update_data(edit_field=None)
        await AdForm.photos.set()
        return

    value = message.text.strip()

    await state.update_data(**{field: value})
    await state.update_data(edit_field=None)

    await message.answer("✅ Изменения сохранены")
    await show_preview(message, state)




async def show_preview(message: types.Message, state: FSMContext):
    data = await state.get_data()

    text = (
        "📋 <b>Проверьте данные объявления:</b>\n\n"
        f"🔹 Тип сделки: {data.get('type')}\n"
        f"🔹 Назначение: {data.get('purpose')}\n"
        f"🔹 Площадь: {data.get('area')} м²\n"
        f"🔹 Район: {data.get('district')}\n"
        f"🔹 Адрес: {data.get('address')}\n"
        f"🔹 Цена: {data.get('price')}\n\n"
        f"📝 Описание:\n{data.get('description')}\n\n"
        f"📞 Контакт: {data.get('contact')}"
    )

    confirm_kb = InlineKeyboardMarkup()
    confirm_kb.add(
        InlineKeyboardButton("✅ Отправить на модерацию", callback_data="send_moderation"),
        InlineKeyboardButton("✏️ Исправить", callback_data="edit_ad")
    )

    await message.answer(text, reply_markup=confirm_kb, parse_mode="HTML")




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

