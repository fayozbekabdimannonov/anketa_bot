from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


builder3 = ReplyKeyboardBuilder()
builder3.row(KeyboardButton(
    text="contact yuborish",
    contact=ReplyKeyboardMarkup(type="contact"))
)
button = builder3.as_markup(resize_keyboard=True)