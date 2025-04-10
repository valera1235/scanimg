from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

import urllib.request

mainmenu = [ [InlineKeyboardButton(text="Отправить изображение",callback_data="sendimg"), InlineKeyboardButton(text="Настройка",callback_data="myoption")] ] # кнопки главного меню
mainmenu = InlineKeyboardMarkup(inline_keyboard=mainmenu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню")]], resize_keyboard=True)

chat_group_dict={} # словарь привязки чата и номера группы

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    greet = "Привет, {name}, я бот, который САМОСТОЯТЕЛЬНО распознает изображения!"
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=mainmenu)

@router.message(F.text == "/menu")
@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
async def menu(msg: Message):
    await msg.answer("Главное меню", reply_markup=mainmenu)


@router.message(F.photo)
async def handle_photo_message(message: Message, state: FSMContext):
    if message.photo:
        file_name = f"photos/{message.photo[-1].file_id}.jpg"
        #await bot.download(message.photo[-1], destination=file_name)
        photo_data = message.photo[-1]
        await message.answer(f'{photo_data}')
        #await message.answer_photo(photo_data.file_id)
        await message.answer("Изображение загружено!")
        print (file_name)
        #recognize_number_with_vgg16(image_path)


@router.callback_query(F.data == "sendimg")
async def sendimg(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    await callback.message.answer("Отправьте изображение, которое необходимо распознать")

@router.callback_query(F.data == "myoption")
async def myoption(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Настройка бота")

@router.message(F.text)
async def message_with_text(msg: Message):
    await msg.answer("Главное меню", reply_markup=mainmenu)
