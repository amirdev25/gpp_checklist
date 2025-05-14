from aiogram import types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from config import CHANNEL_ID
from states import RegisterState
from aiogram.fsm.context import FSMContext


router = Router()

kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="check_sub")]
            ])

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        member = await message.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "creator", "administrator"]:
            await message.answer("Ism va familiyangizni kiriting:")
            await state.set_state(RegisterState.full_name)
        else:
            await message.answer(f"Botdan foydalanish uchun avval {CHANNEL_ID} kanaliga obuna bo‘ling.", reply_markup=kb)
    except Exception as e:
        await message.answer("Obuna holatini tekshirib bo‘lmadi. Qayta urinib ko‘ring.")
        print("Start check error:", e)

@router.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        member = await callback.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "creator", "administrator"]:
            await callback.message.answer("Ism va familiyangizni kiriting:")
            await state.set_state(RegisterState.full_name)
        else:
            await callback.message.answer(f"Kechirasiz, siz hali obuna bo‘lmagansiz. \n\nIltimos, Botdan foydalanish uchun avval {CHANNEL_ID} kanaliga obuna bo‘ling.", reply_markup=kb)
    except Exception as e:
        await callback.message.answer("Obuna holatini tekshirishda xatolik yuz berdi. Qayta urinib ko‘ring.")
        print("check_sub xatolik:", e)
