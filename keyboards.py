from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from config import (
    TODAY_BUTTON,
    YESTERDAY_BUTTON,
    SEND_CONTACT_BUTTON,
    PROJECTS_BUTTON,
    OSNOVA_BUTTON,
    CONTRACTOR_BUTTON,
    project_id_regex,
)


async def get_contact_markup() -> ReplyKeyboardMarkup:
    get_contact = KeyboardButton(SEND_CONTACT_BUTTON, request_contact=True)
    custom_keyboard = [[get_contact]]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)


async def projects_markup(projects: list) -> InlineKeyboardMarkup:
    keyboard = []
    for project in projects:
        name = project["name"][:40]
        # slice coz TGAPI recieved only 64bytes on callback
        callback_data = f"{project['name'][:10]}{project_id_regex}{project['id']}"
        keyboard.append([InlineKeyboardButton(name, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)


async def main_markup() -> ReplyKeyboardMarkup:
    projects_button = KeyboardButton(PROJECTS_BUTTON)
    custom_keyboard = [[projects_button]]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)


async def projects_detail_markup(is_employee: bool = False) -> ReplyKeyboardMarkup:
    yesterday_button = KeyboardButton(YESTERDAY_BUTTON)
    today_button = KeyboardButton(TODAY_BUTTON)
    projects_button = KeyboardButton(PROJECTS_BUTTON)
    osnova_button = KeyboardButton(OSNOVA_BUTTON)
    custom_keyboard = [
        [yesterday_button, today_button],
        [projects_button],
    ]
    if is_employee:
        custom_keyboard = [
            [yesterday_button, today_button, osnova_button],
            [projects_button],
        ]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)


async def osnova_detail_markup() -> ReplyKeyboardMarkup:
    yesterday_button = KeyboardButton(YESTERDAY_BUTTON)
    today_button = KeyboardButton(TODAY_BUTTON)
    constractor_button = KeyboardButton(CONTRACTOR_BUTTON)
    projects_button = KeyboardButton(PROJECTS_BUTTON)
    custom_keyboard = [
        [yesterday_button, today_button],
        [constractor_button],
        [projects_button],
    ]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
