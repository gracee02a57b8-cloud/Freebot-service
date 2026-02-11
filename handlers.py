from telegram import Update
from telegram.ext import ContextTypes

from messages import (
    project_yesterday_message,
    project_today_message,
    osnova_today_message,
    osnova_yesterday_message,
)
from db import set_number, get_project_id, set_project_id, set_user_is_employee, get_user_is_employee, add_project, get_project_name
from auth import is_auth_user, _check_auth
from backend import (
    _get_project_yesterday,
    _backend_get_projects,
    _get_project_today,
    _get_osnova_today,
    _get_osnova_yesterday,
)
from keyboards import (
    main_markup,
    projects_markup,
    projects_detail_markup,
    get_contact_markup,
    osnova_detail_markup,
)

from config import (
    HI_TEXT,
    CHOOSE_PERIOD,
    TODAY_BUTTON,
    UNAUTH_TEXT,
    YESTERDAY_BUTTON,
    SEND_CONTACT_TEXT,
    SET_PROJECT_TEXT,
    PROJECTS_BUTTON,
    CONTRACTOR_BUTTON,
    PROJECTS,
    OSNOVA_BUTTON,
    OSNOVA_HELLO,
    project_id_regex,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = await get_contact_markup()
    await update.message.reply_text(SEND_CONTACT_TEXT, reply_markup=reply_markup)


@is_auth_user
async def projects(
    update: Update, context: ContextTypes.DEFAULT_TYPE, phone_number: str
):
    projects, osnova_access = await _backend_get_projects(phone_number)

    user_id = update.message.from_user.id
    await set_user_is_employee(user_id, osnova_access)

    for project in projects:
        await add_project(project["id"], project["name"])

    reply_markup = await projects_markup(projects)
    await update.message.reply_text(PROJECTS, reply_markup=reply_markup)


@is_auth_user
async def project_today(
    update: Update, context: ContextTypes.DEFAULT_TYPE, phone_number: str
):
    user_id = update.message.from_user.id
    project_id, is_osnova = await get_project_id(user_id)

    if is_osnova:
        info = await _get_osnova_today(phone_number, project_id)
        result = await osnova_today_message(info)
    else:
        info = await _get_project_today(phone_number, project_id)
        result = await project_today_message(info)

    await update.message.reply_text(result, parse_mode="Markdown")


@is_auth_user
async def project_yesterday(
    update: Update, context: ContextTypes.DEFAULT_TYPE, phone_number: str
):
    user_id = update.message.from_user.id
    project_id, is_osnova = await get_project_id(user_id)

    if is_osnova:
        info = await _get_osnova_yesterday(phone_number, project_id)
        result = await osnova_yesterday_message(info)
    else:
        info = await _get_project_yesterday(phone_number, project_id)
        result = await project_yesterday_message(info)

    await update.message.reply_text(result, parse_mode="Markdown")


@is_auth_user
async def osnova_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE, phone_number: str
):
    user_id = update.message.from_user.id
    project_id, _ = await get_project_id(user_id)
    await set_project_id(user_id, project_id, True)
    reply_markup = await osnova_detail_markup()
    await update.message.reply_text(OSNOVA_HELLO, reply_markup=reply_markup)


@is_auth_user
async def constractor_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE, phone_number: str
):
    user_id = update.message.from_user.id
    project_id, _ = await get_project_id(user_id)
    await set_project_id(user_id, project_id, False)
    is_employee = await get_user_is_employee(user_id)
    reply_markup = await projects_detail_markup(is_employee)
    await update.message.reply_text(CHOOSE_PERIOD, reply_markup=reply_markup)


async def get_contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    auth: bool = await _check_auth(update.message.contact.phone_number)
    if not auth:
        await update.message.reply_text(UNAUTH_TEXT)
        return

    await set_number(
        id=update.message.from_user.id,
        phone_number=update.message.contact.phone_number,
    )
    keyboard = await main_markup()
    await update.message.reply_text(
        HI_TEXT, reply_markup=keyboard, parse_mode="Markdown"
    )


@is_auth_user
async def select_project_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE, phone_number: str
):
    user_id = update.callback_query.from_user.id
    message_text = update.callback_query.data
    if project_id_regex not in message_text:
        return

    project_id = message_text[message_text.find(project_id_regex) + 4 :]
    await set_project_id(
        user_id=user_id, project_id=project_id
    )

    project_name = await get_project_name(project_id)

    await update.callback_query.edit_message_text(
        f"{SET_PROJECT_TEXT} {project_name}.", parse_mode="Markdown"
    )
    is_employee = await get_user_is_employee(user_id)
    markup = await projects_detail_markup(is_employee)
    await update.callback_query.message.reply_text(CHOOSE_PERIOD, reply_markup=markup)


async def common_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # exit from common_callback if this is query
    if not update.message:
        return
    # check phone number
    if getattr(update.message, "contact"):
        await get_contact_handler(update, context)

    # projects info
    if update.message.text == PROJECTS_BUTTON:
        await projects(update=update, context=context)
    # project today info
    if update.message.text == TODAY_BUTTON:
        await project_today(update=update, context=context)
    # project yesterday info
    if update.message.text == YESTERDAY_BUTTON:
        await project_yesterday(update=update, context=context)
    # set osnova
    if update.message.text == OSNOVA_BUTTON:
        await osnova_button(update=update, context=context)
    # unset osnova
    if update.message.text == CONTRACTOR_BUTTON:
        await constractor_button(update=update, context=context)
