from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from states import RegisterState
from db import save_user
from config import PDF_FILE_PATH
from config import ADMIN_GROUP_ID
from datetime import datetime

router = Router()

@router.message(RegisterState.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=kb)
    await state.set_state(RegisterState.phone)

@router.message(RegisterState.phone)
async def phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Dorixona egasi", callback_data="Dorixona egasi")],
        [InlineKeyboardButton(text="HR mutaxassis", callback_data="HR mutaxassis")],
        [InlineKeyboardButton(text="Farmatsevt mutaxassis", callback_data="Farmatsevt mutaxassis")],
        [InlineKeyboardButton(text="Boshqa", callback_data="Boshqa")]
    ])
    await message.answer("Kasbingizni tanlang:", reply_markup=kb)
    await state.set_state(RegisterState.job)

@router.callback_query(RegisterState.job)
async def job(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(job=callback.data)
    data = await state.get_data()

    # 1. Ma’lumotlarni DBga yozamiz
    await save_user(callback.from_user.id, data['full_name'], data['phone'], data['job'])

    # 2. Admin guruhga xabar yuboramiz
    register_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    admin_msg = (
        "<b>New lead:</b>\n"
        f"<b>Name:</b> {data['full_name']}\n"
        f"<b>Phone:</b> {data['phone']}\n"
        f"<b>Job:</b> {data['job']}\n"
        f"<b>Register time:</b> {register_time}"
    )
    await callback.bot.send_message(chat_id=ADMIN_GROUP_ID, text=admin_msg, parse_mode="HTML")

    # 3. Tugmalarni edit qilamiz
    await callback.message.edit_text("✅ Rahmat! Ma'lumotlaringiz qabul qilindi.")

    # 4. PDF fayl yuboramiz
    await callback.message.answer_document(FSInputFile(PDF_FILE_PATH), caption="Mana sizga va'da qilingan checklist!")

    await state.clear()

@router.message()
async def fallback_handler(message: types.Message):
    await message.answer(
        "GPP kursiga yozilish uchun quyidagi havolani bosing:\n"
        "https://forms.amocrm.ru/rwtzmzl"
    )

