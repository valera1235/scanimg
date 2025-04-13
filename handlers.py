from aiogram import F, Router
from aiogram import Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from config import TOKEN
from scanimg import recognize_number_with_vgg16
from easyocr import recognize_numbers_with_easyocr

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
        bot = Bot(token=TOKEN)
        file = await bot.get_file(message.photo[-1].file_id)
        await message.answer("Изображение загружено!")
        image_path =  "https://api.telegram.org/file/bot" + TOKEN + "/"+file.file_path
        await message.answer(image_path)
        #answer = recognize_number_with_vgg16(image_path)
        #answer = recognize_numbers_with_easyocr(image_path)
        await message.answer(answer)

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
