from db import get_number
from backend import has_access


async def _check_auth(phone_number):
    access: bool = await has_access(phone_number)
    return access


def is_auth_user(func):
    async def wrapper(*args, **kwargs):
        update = kwargs.get("update")
        if not update:
            update = args[0]
            user_id: int = update.callback_query.from_user.id
        else:
            user_id: int = update.message.from_user.id
        kwargs["phone_number"] = await get_number(user_id)
        if kwargs["phone_number"]:
            return await func(*args, **kwargs)

    return wrapper
