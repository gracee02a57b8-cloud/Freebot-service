from telegram import Update
from telegram.ext import Application, CommandHandler, TypeHandler, CallbackQueryHandler

from config import TELEGRAM_TOKEN
from handlers import common_callback, start, select_project_button


def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(select_project_button))
    handler = TypeHandler(Update, common_callback)
    application.add_handler(handler, -1)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
