import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputMediaPhoto, InputMediaVideo

API_TOKEN = os.getenv("BOT_TOKEN")

MODERATION_CHAT_ID = -1003846593729

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def media_done_inline_kb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ Готово", callback_data="media_done")
    )
    return kb




# =========================
# НИЖНЕЕ МЕНЮ
# =========================

# keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard.add("Разместить объявление")
# keyboard.add("Связаться с администратором")
# keyboard.add("ПРОДАЖА смотреть объявления")
# keyboard.add("АРЕНДА смотреть объявления")


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
    media = State()
    price = State()
    contact_method = State()
    contact = State()
    preview = State()
    edit = State()



# =========================
# INLINE-КЛАВИАТУРА ГЛАВНОГО МЕНЮ
# =========================

def main_menu_inline_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Разместить объявление", callback_data="menu_add"),
        InlineKeyboardButton("Связаться с администратором", callback_data="menu_contact"),
        InlineKeyboardButton("ПРОДАЖА смотреть объявления", callback_data="menu_sale"),
        InlineKeyboardButton("АРЕНДА смотреть объявления", callback_data="menu_rent"),
    )
    return kb





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
        InlineKeyboardButton("Медиа", callback_data="edit_media"),
    )
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="edit_back")
    )
    return kb


# =========================
# inline-кнопка «Отмена»
# =========================

def cancel_inline_kb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("❌ Отмена", callback_data="cancel_ad")
    )
    return kb


# =========================
# Функции валидации
# =========================

import re

def is_phone(text: str) -> bool:
    text = text.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return bool(re.fullmatch(r"(\+7|7|8)\d{10}", text))

def is_username(text: str) -> bool:
    return bool(re.fullmatch(r"@[A-Za-z0-9_]{5,32}", text))


# =========================
# /start
# =========================

@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Добро пожаловать!\nВыберите действие:",
        reply_markup=main_menu_inline_kb()
    )




@dp.callback_query_handler(
    lambda c: c.data.startswith("menu_"),
    state="*"
)
async def main_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    if callback.data == "menu_add":
        await start_ad_flow(callback.message, state)

    elif callback.data == "menu_contact":
        await callback.message.answer(
            "📞 Контакты администратора:\n\n"
            "Телефон: +7 938 400-05-58\n"
            "Telegram: https://t.me/moder_com"
        )

    elif callback.data == "menu_sale":
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Открыть объявления о продаже",
                url="https://t.me/sochi_commerc/4"
            )
        )
        await callback.message.answer(
            "Продажа коммерческой недвижимости:",
            reply_markup=kb
        )

    elif callback.data == "menu_rent":
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Открыть объявления об аренде",
                url="https://t.me/sochi_commerc/3"
            )
        )
        await callback.message.answer(
            "Аренда коммерческой недвижимости:",
            reply_markup=kb
        )


# =========================
# /cancel
# =========================

@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Действие отменено.\nВыберите действие:",
        reply_markup=main_menu_inline_kb()
    )


# =========================
# СВЯЗЬ С АДМИНИСТРАТОРОМ
# =========================

@dp.message_handler(lambda m: m.text == "Связаться с администратором", state="*")
async def contact_admin(message: types.Message):
    await message.answer(
        "📞 Контакты администратора:\n\n"
        "Телефон: +7 938 400-05-58\n"
        "Telegram: https://t.me/moder_com\n" 
       
    )


# =========================
# ПРОДАЖА
# =========================

@dp.message_handler(lambda m: m.text == "ПРОДАЖА смотреть объявления", state="*")
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

@dp.message_handler(lambda m: m.text == "АРЕНДА смотреть объявления", state="*")
async def rent(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="Открыть объявления об аренде",
            url="https://t.me/sochi_commerc/3"
        )
    )
    await message.answer("Аренда коммерческой недвижимости:", reply_markup=kb)



# =========================
# РАЗМЕСТИТЬ ОБЪЯВЛЕНИЕ
# =========================


async def start_ad_flow(message: types.Message, state: FSMContext):
    await state.finish()  # ← КЛЮЧЕВО
    await message.answer(
        "Выберите тип сделки:",
        reply_markup=deal_type_kb()
    )
    await AdForm.deal_type.set()


@dp.message_handler(lambda m: m.text == "Разместить объявление", state="*")
async def add_ad_start(message: types.Message, state: FSMContext):
    await start_ad_flow(message, state)



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
    await state.update_data(media=[])
    await message.answer(
        "Добавьте фото и/или видео объекта (до 10 шт)."          
    )
    await AdForm.media.set()


@dp.message_handler(
    content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO],
    state=AdForm.media
)
async def process_media(message: types.Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])

    if len(media) >= 10:
        await message.answer("⛔ Можно добавить не более 10 файлов.")
        return

    if message.content_type == types.ContentType.PHOTO:
        media.append({
            "type": "photo",
            "file_id": message.photo[-1].file_id
        })
    else:
        media.append({
            "type": "video",
            "file_id": message.video.file_id
        })

    await state.update_data(media=media)

    await message.answer(
        f"✅ Добавлено ({len(media)}/10)\n\nДобавьте ещё или нажмите «Готово»",
        reply_markup=media_done_inline_kb()
    )




@dp.callback_query_handler(lambda c: c.data == "media_done", state=AdForm.media)
async def media_done(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()

    if not data.get("media"):
        await callback.message.answer("❗ Добавьте хотя бы одно фото или видео.")
        return

    await callback.message.answer("Введите цену объекта:")
    await AdForm.price.set()



    # клавиатура контакта

@dp.message_handler(state=AdForm.price)
async def process_price(message: types.Message, state: FSMContext):
    price = message.text.strip()
    await state.update_data(price=price)

    username = message.from_user.username
    hint = ""

    if username:
        hint = f"\n\n💡 Вы можете просто отправить: @{username}"

    await message.answer(
        "📞 Укажите контакт для связи:\n\n"
        "Можно указать:\n"
        "• телефон\n"
        "• @username\n"
        "• WhatsApp / Telegram"
        f"{hint}"
    )

    await AdForm.contact.set()




@dp.callback_query_handler(
    lambda c: c.data == "contact_share",
    state=AdForm.contact_method
)
async def contact_share(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer(
        "Пожалуйста, отправьте контакт, используя кнопку «Поделиться контактом» "
        "в Telegram или введите номер вручную."
    )


@dp.callback_query_handler(
    lambda c: c.data == "contact_manual",
    state=AdForm.contact_method
)
async def contact_manual(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer(
        "Введите контакт для связи в свободной форме:"
    )

    await AdForm.contact.set()



  
@dp.message_handler(
    content_types=types.ContentType.CONTACT,
    state=AdForm.contact_method
)
async def process_contact_share(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    await state.update_data(contact=contact)

    await show_preview(message, state)
    await AdForm.preview.set()



@dp.message_handler(state=AdForm.contact)
async def process_contact_manual(message: types.Message, state: FSMContext):
    contact = message.text.strip()

    if len(contact) < 5:
        await message.answer(
            "❗ Контакт слишком короткий.\n"
            "Пожалуйста, укажите телефон или @username."
        )
        return

    warning = ""
    if not is_phone(contact) and not is_username(contact):
        warning = (
            "\n\n⚠️ Обратите внимание:\n"
            "Формат контакта нестандартный, но мы всё равно сохранили его."
        )

    await state.update_data(contact=contact)

    if warning:
        await message.answer(warning)

    await show_preview(message, state)
    await AdForm.preview.set()




@dp.callback_query_handler(lambda c: c.data == "edit_ad", state=AdForm.preview)
async def edit_ad(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "Что Вы хотите исправить?",
        reply_markup=edit_menu_kb()
    )
    await AdForm.edit.set()



@dp.callback_query_handler(lambda c: c.data == "send_moderation", state=AdForm.preview)
async def send_to_moderation(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    media = data.get("media", [])

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

    moderation_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Одобрить", callback_data="approve_ad"),
        InlineKeyboardButton("Отклонить", callback_data="reject_ad")
    )

    # 1️⃣ сначала текст + кнопки
    await bot.send_message(
        MODERATION_CHAT_ID,
        text,
        reply_markup=moderation_kb,
        parse_mode="HTML"
    )

    # 2️⃣ затем альбом (ОДНО объявление, НЕ несколько)
    if media:
        album = []
        for item in media:
            if item["type"] == "photo":
                album.append(InputMediaPhoto(media=item["file_id"]))
            elif item["type"] == "video":
                album.append(InputMediaVideo(media=item["file_id"]))

        await bot.send_media_group(
            chat_id=MODERATION_CHAT_ID,
            media=album
        )

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



@dp.callback_query_handler(lambda c: c.data.startswith("edit_"), state=AdForm.edit)
async def choose_edit_field(callback: types.CallbackQuery, state: FSMContext):
    field = callback.data.replace("edit_", "")

    if field == "back":
        await callback.answer()
        await show_preview(callback.message, state)
        await AdForm.preview.set()
        return

    await state.update_data(edit_field=field)
    await callback.answer()

    prompts = {
        "type": "Введите новый тип сделки:",
        "purpose": "Введите новое назначение:",
        "area": "Введите новую площадь:",
        "district": "Введите новый район:",
        "address": "Введите новый адрес:",
        "description": "Введите новое описание:",
        "price": "Введите новую цену:",
        "media": "Отправьте новые фото (старые будут удалены)",
    }

    await callback.message.answer(prompts[field])



@dp.message_handler(state=AdForm.edit)
async def process_edit_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("edit_field")

    if not field:
        return

    value = message.text.strip()
    if not value:
        await message.answer("❗ Значение не может быть пустым")
        return

    await state.update_data(**{field: value})
    await state.update_data(edit_field=None)

    await message.answer("✅ Изменения сохранены")
    await show_preview(message, state)
    await AdForm.preview.set()




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
        InlineKeyboardButton("Отправить на модерацию", callback_data="send_moderation"),
        InlineKeyboardButton("Исправить", callback_data="edit_ad")
    )

    # 1️⃣ текст
    await message.answer(text, parse_mode="HTML")

    # 2️⃣ альбом
    media = data.get("media", [])
    if media:
        album = []
        for item in media:
            if item["type"] == "photo":
                album.append(InputMediaPhoto(media=item["file_id"]))
            elif item["type"] == "video":
                album.append(InputMediaVideo(media=item["file_id"]))

        await message.answer_media_group(album)

    # 3️⃣ кнопки
    await message.answer(
        "Всё верно?",
        reply_markup=confirm_kb
    )

@dp.callback_query_handler(lambda c: c.data == "cancel_ad", state="*")
async def cancel_ad_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Отменено")
    await state.finish()

    await callback.message.answer(
        "❌ Размещение объявления отменено.\n\n"
        "Выберите действие:",
        reply_markup=main_menu_inline_kb()
    )


# =========================
# ЗАПУСК
# =========================

# asyncio.get_event_loop().run_until_complete(send_post_button_once())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
