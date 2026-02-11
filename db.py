from pymongo import MongoClient
from config import MONGO_DB_URI, MONGO_NAME, logger

# database schema
#     state: id, project_id, is_osnova
#     user: id, phone_number, is_employee
#     project: id, project_name


async def connection():
    client = MongoClient(MONGO_DB_URI, authSource="admin")
    mydb = client[MONGO_NAME]
    return mydb


async def get_project_id(user_id: int) -> tuple[str, bool]:
    logger.info(f"Get project_id by user id {user_id}")
    db = await connection()
    db = db["state"]
    res = db.find_one({"_id": user_id})
    if res:
        return res.get("project_id"), res.get("is_osnova")
    return


async def set_project_id(user_id: str, project_id: str, is_osnova: bool = False):
    logger.info(f"Set project_id {project_id} for user_id {user_id}")
    db = await connection()
    db = db["state"]
    if await get_project_id(user_id):
        state = {"$set": {"project_id": project_id, "is_osnova": is_osnova} }
        res = db.update_one({"_id": user_id}, state)
    else:
        state: dict = {"_id": user_id, "project_id": project_id}
        res = db.insert_one(state)


async def get_number(user_id: int) -> str:
    logger.info(f"Get number by user id {user_id}")
    db = await connection()
    db = db["users"]
    res = db.find_one({"_id": user_id})
    if res:
        return res.get("phone_number")
    return


async def set_number(id: str, phone_number: str):
    logger.info(f"Set number #### for user_id {id}")
    if await get_number(id):
        return
    if "+" in phone_number:
        phone_number = phone_number[1:]
    user: dict = {"_id": id, "phone_number": phone_number}
    db = await connection()
    db = db["users"]
    res = db.insert_one(user)


async def set_user_is_employee(user_id: str, is_employee: bool = False):
    logger.info(f"Set is_employee = {is_employee} for user_id {user_id}")
    db = await connection()
    db = db["users"]
    state = {"$set": {"is_employee": is_employee}}
    res = db.update_one({"_id": user_id}, state)


async def get_user_is_employee(user_id: str):
    logger.info(f"Get is_employee for user_id {user_id}")
    db = await connection()
    db = db["users"]
    res = db.find_one({"_id": user_id})
    if res:
        return res.get("is_employee")


async def add_project(project_id: int, project_name: str):
    logger.info(f"Set project_name {project_name} for project_id {project_id}")
    db = await connection()
    db = db["projects"]
    res = db.find_one({"_id": int(project_id)})

    if res:
        project = {"$set": {"project_name": project_name} }
        res = db.update_one({"_id": int(project_id)}, project)
    else:
        project: dict = {"_id": int(project_id), "project_name": project_name}
        res = db.insert_one(project)


async def get_project_name(project_id: int) -> str:
    logger.info(f"Get project_name for project_id {project_id}")
    db = await connection()
    db = db["projects"]
    res = db.find_one({"_id": int(project_id)})
    return res.get("project_name") if res else ''
