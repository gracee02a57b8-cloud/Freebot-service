import httpx

from config import BACKEND_BASE_URL, REQUEST_TIMEOUT, logger

timeout = httpx.Timeout(REQUEST_TIMEOUT, connect=10)


async def _backend_get_projects(phone_number) -> dict:
    logger.info(f"Get projects info {phone_number}")
    url = BACKEND_BASE_URL + "/api/projects/"
    headers = {"Authorization": phone_number}
    response = httpx.get(url, headers=headers, verify=False, timeout=timeout)

    access_header = response.headers["osnova-access"]
    osnova_access = True if access_header == "True" else False

    return response.json(), osnova_access


async def _get_project_today(phone_number, project_id) -> dict:
    logger.info(f"Get today info for project {project_id}")
    url = BACKEND_BASE_URL + f"/api/builders/persons-info/{project_id}/today"
    headers = {"Authorization": phone_number}
    response = httpx.get(url, headers=headers, verify=False, timeout=timeout)
    return response.json()


async def _get_project_yesterday(phone_number, project_id) -> dict:
    logger.info(f"Get yesterday info for project {project_id}")
    url = BACKEND_BASE_URL + f"/api/builders/persons-info/{project_id}/yesterday"
    headers = {"Authorization": phone_number}
    response = httpx.get(url, headers=headers, verify=False, timeout=timeout)
    return response.json()


async def _get_osnova_today(phone_number, project_id) -> dict:
    logger.info(f"Get osnova today info for project {project_id}")
    url = BACKEND_BASE_URL + f"/api/employees/osnova-info/{project_id}/today"
    headers = {"Authorization": phone_number}
    response = httpx.get(url, headers=headers, verify=False, timeout=timeout)
    return response.json()


async def _get_osnova_yesterday(phone_number, project_id) -> dict:
    logger.info(f"Get osnova yesterday info for project {project_id}")
    url = BACKEND_BASE_URL + f"/api/employees/osnova-info/{project_id}/yesterday"
    headers = {"Authorization": phone_number}
    response = httpx.get(url, headers=headers, verify=False, timeout=timeout)
    return response.json()


async def has_access(phone_number) -> bool:
    logger.info(f"Check access for {phone_number}")
    if "+" in phone_number:
        phone_number = phone_number[1:]
    url = BACKEND_BASE_URL + "/api/users/has-access"
    params = {"userPhone": phone_number}
    response = httpx.get(url, params=params, verify=False, timeout=timeout)
    if response.status_code == httpx.codes.OK:
        return bool(response.json())
    return False
