from datetime import datetime


async def pretty_time(time: str) -> str:
    date = datetime.strptime(time[:-6], "%Y-%m-%dT%H:%M:%S")
    return date.strftime("%H:%M")


async def pretty_time_info(employ: dict) -> str:
    arrivalTime = employ.get("arrivalTime")
    exitTime = employ.get("exitTime")
    if arrivalTime and exitTime:
        arrivalTime = await pretty_time(arrivalTime)
        exitTime = await pretty_time(exitTime)
        return f"{arrivalTime} - {exitTime}"

    if arrivalTime and not exitTime:
        arrivalTime = await pretty_time(arrivalTime)
        return f"{arrivalTime} - ..."

    if not arrivalTime and exitTime:
        exitTime = await pretty_time(exitTime)
        return f"... - {exitTime}"


async def pretty_summary(count) -> str:
    if count > 1 and count < 5:
        return f"*Итого: {count} человека*"
    return f"*Итого: {count} человек*"


async def project_yesterday_message(info: dict) -> str:
    text = f"*{info['projectName']}*\nСтатистика вчера:\n\n"
    for stat in info["statistics"]:
        builder = stat["builderName"]
        lots = str(stat["lots"])
        personsCount = str(stat["personsCount"])
        personsPerDay = str(round(stat["personsPerDay"], 2))
        times = personsCount + " чел / " + personsPerDay + " ч.ч."

        text += f"*{builder} - {times}*\n[{lots}]\n\n"
    summaryPersonsCount = str(info["summaryPersonsCount"])
    summaryPersonsPerDay = str(round(info["summaryPersonsPerDay"], 2))
    text += f"*Итого: {summaryPersonsCount} чел / {summaryPersonsPerDay} ч.ч.*"

    button_passes_in = info["buttonPasses"]["in"]   
    button_passes_out = info["buttonPasses"]["out"]
    if button_passes_in + button_passes_out != 0:
        text += "\n\n*Проходы по кнопке:*"
        text += f'\n*Вход: {info["buttonPasses"]["in"]} чел*'
        text += f'\n*Выход: {info["buttonPasses"]["out"]} чел*'

    unlocked_passes_in = info["unlockedPasses"]["in"]
    unlocked_passes_out = info["unlockedPasses"]["out"]
    if unlocked_passes_in + unlocked_passes_out != 0:
        text += "\n\n*Проходы через разблокированный турникет:*"
        text += f'\n*Вход: {unlocked_passes_in} чел*'
        text += f'\n*Выход: {unlocked_passes_out} чел*'

    return text


async def project_today_message(info: dict) -> str:
    text = f"*{info['projectName']}*\nСтатистика сейчас:\n\n"
    for stat in info["statistics"]:
        builder = stat["builderName"]
        lots = str(stat["lots"])
        times = str(stat["personsCount"]) + " чел"

        text += f"*{builder} - {times}*\n[{lots}]\n\n"
    text += await pretty_summary(info["summaryPersonsCount"])

    button_passes_in = info["buttonPasses"]["in"]   
    button_passes_out = info["buttonPasses"]["out"]
    if button_passes_in + button_passes_out != 0:
        text += "\n\n*Проходы по кнопке:*"
        text += f'\n*Вход: {info["buttonPasses"]["in"]} чел*'
        text += f'\n*Выход: {info["buttonPasses"]["out"]} чел*'

    unlocked_passes_in = info["unlockedPasses"]["in"]
    unlocked_passes_out = info["unlockedPasses"]["out"]
    if unlocked_passes_in + unlocked_passes_out != 0:
        text += "\n\n*Проходы через разблокированный турникет:*"
        text += f'\n*Вход: {unlocked_passes_in} чел*'
        text += f'\n*Выход: {unlocked_passes_out} чел*'

    return text


async def osnova_today_message(info: dict) -> str:
    summaryPersonsCount = 0
    text = f'*{info["projectName"]}*\nСтатистика "Основа" сейчас:\n\n'
    for employ in info["employees"]:
        summaryPersonsCount += 1
        name = employ["fullName"]
        arrival = await pretty_time(employ["arrivalTime"])
        text += f"*{name}* \[ {arrival} ]\n"
    text += await pretty_summary(summaryPersonsCount)
    return text


async def osnova_yesterday_message(info: dict) -> str:
    summaryPersonsCount = 0
    text = f'*{info["projectName"]}*\nСтатистика "Основа" вчера:\n\n'
    for employ in info["employees"]:
        summaryPersonsCount += 1
        name = employ["fullName"]
        time_text = await pretty_time_info(employ)
        text += f"*{name}* \[ {time_text} ]\n"
    text += await pretty_summary(summaryPersonsCount)
    return text
