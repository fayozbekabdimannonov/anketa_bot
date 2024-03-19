import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.types import Message
from data.create import create_anketa,anketa_qushish,users_id
from aiogram.fsm.context import FSMContext
from states.anketa import AnketaState #new
from states.anketa import AnketaState #new
import re


# TOKEN = "6595492047:AAHBwg4xGuONGDQCE-5hFgHTccsp--6xp10" #Token kiriting
# ADMINS = [6109857994]

# dp = Dispatcher()

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,CallbackQuery,ReplyKeyboardRemove
import config
import asyncio
import logging
import sys


from kanal_filtr import IsCheckSubChannels

from aiogram.fsm.context import FSMContext #new

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time 
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()



@dp.message(F.forward_from_chat)
async def kanal_id_olish(message:Message):
    text  = str(message.forward_from_chat.id)
    await message.answer(text)

@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        # db.add_user(full_name=full_name,telegram_id=telegram_id)
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz")
    except:
        await message.answer(text="Assalomu alaykum", reply_markup=ReplyKeyboardRemove)



@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext):
    idlar = [id[0] for id in users_id()]
    telegram_id = message.from_user.id
    if telegram_id in idlar:
        await message.answer("Xush kelibsiz")
    else:
        await state.set_state(AnketaState.ism)
        text="Assalomu alaykum, Anketa botimizga hush kelibsiz!\nRo'yxatdan o'tish uchun ismingizni kiriting"
        await message.answer(text)

@dp.message(F.text,AnketaState.ism)
async def ismni_olish(message:Message,state:FSMContext):
    await state.set_state(AnketaState.familya)
    ism = message.text
    await state.update_data(ism=ism)
    text="Familyangizni kiriting"
    await message.answer(text) 

@dp.message(F.text,AnketaState.familya)
async def familyani_olish(message:Message,state:FSMContext):
    await state.set_state(AnketaState.tel_raqam)
    familya = message.text
    await state.update_data(familya=familya)
    text="telefon raqamingizni kiriting"
    await message.answer(text) 

@dp.message(F.text,AnketaState.tel_raqam)
async def phone_number_register(message:Message,state:FSMContext):
    tel_raqam = message.text
    pattern = re.compile("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")
    if pattern.match(tel_raqam):
        await state.update_data(tel_raqam = tel_raqam)
        await state.set_state(AnketaState.jinsi)
        await message.answer(text="jinsingizni kiriting")
    else:
        await message.answer(text="Telefon raqamingiz noto`gri.iltimos qayta kiritng")

@dp.message(F.text,AnketaState.jinsi)
async def familyani_olish(message:Message,state:FSMContext):
    await state.set_state(AnketaState.t_yil)
    jinsi = message.text
    await state.update_data(jinsi=jinsi)
    text="  tug`ulgan yilingizni kiriting"
    await message.answer(text) 




@dp.message(F.text,AnketaState.t_yil)
async def yilni_olish(message:Message,state:FSMContext):
    t_yil = message.text
    if t_yil.isdigit():
        await state.set_state(AnketaState.t_oy)
        await state.update_data(t_yil=t_yil)
        text="Tug'ilgan oyingizni kiriting"
        await message.answer(text) 
    else:
        await message.answer("qayta kiriting") 

@dp.message(F.text,AnketaState.t_oy)
async def oy_olish(message:Message,state:FSMContext):
    
    
    t_oy = message.text
    if t_oy.isdigit():
        await state.set_state(AnketaState.t_kun)
        await state.update_data(t_oy=t_oy)
        text="Tug'ilgan kuningizni kiriting"
        await message.answer(text) 
    else:
        await message.answer("qayta kiriting") 

@dp.message(F.text,AnketaState.t_kun)
async def kun_olish(message:Message,state:FSMContext):
    
    t_kun = message.text
    if t_kun.isdigit():
        await state.set_state(AnketaState.rasm)
        await state.update_data(t_kun=t_kun)
        text="Rasm yuboring"
        await message.answer(text) 
    else:
        await message.answer("qayta kiriting") 

@dp.message(F.photo,AnketaState.rasm)
async def rasm_olish(message:Message,state:FSMContext):
    
    rasm = message.photo[-1].file_id
    data = await state.get_data()
    ism = data.get("ism")
    familya = data.get("familya")
    tel_raqam = data.get("tel_raqam")
    jinsi = data.get("jinsi")
    t_yil = data.get("t_yil")
    t_oy = data.get("t_oy")
    t_kun = data.get("t_kun")
    telegram_id = message.from_user.id
    anketa_qushish(ism,familya,tel_raqam,jinsi,t_yil,t_oy,t_kun,rasm,telegram_id)
    await message.answer("ro'yhatdan o'tdingiz") 
    await state.clear()
    

#bot ishga tushganini xabarini yuborish
@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    create_anketa()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
