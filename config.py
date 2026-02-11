import os
import dotenv
import logging


YESTERDAY_BUTTON: str = "Вчера"
TODAY_BUTTON: str = "Сейчас"
PROJECTS_BUTTON: str = "Выбрать проект"
OSNOVA_BUTTON: str = "ОСНОВА"
CONTRACTOR_BUTTON: str = "Подрядчики"
CHOOSE_PERIOD: str = "Для просмотра статистики выберите период."
OSNOVA_HELLO: str = "Выбран просмотр статистики по сотрудникам ГК Основа."
HI_TEXT: str = "Авторизация выполнена. Для продолжения нажмите \"Выбрать проект\"."
SET_PROJECT_TEXT: str = "Вы выбрали проект"
PROJECTS: str = "Проекты:"
UNAUTH_TEXT: str = "Для указанного номера телефона доступа нет. По вопросам предоставления доступа обращайтесь на 0000@gk-osnova.ru."
SEND_CONTACT_BUTTON: str = "Поделиться контактом"
SEND_CONTACT_TEXT: str = (
    "Требуется авторизация для просмотра статистики.\nНажмите кнопку \"Поделиться контактом\".\nПодтвердите действие в появившемся окне."
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
BACKEND_BASE_URL: str = os.getenv("BACKEND_BASE_URL")
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT"))

MONGO_HOST: str = os.getenv("MONGO_HOST")
MONGO_PORT: str = os.getenv("MONGO_PORT")
MONGO_USERNAME: str = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD")
MONGO_NAME: str = os.getenv("MONGO_NAME")
MONGO_DB_URI: str = (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_NAME}"
)


# regex
project_id_regex: str = ";id:"
