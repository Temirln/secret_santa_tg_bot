from aiogram.utils.markdown import hbold


start_text_private = """
Приветсвую <b>{user_name}</b> , 
Добро Пожаловать в Телеграм Бота 
Secret Santa Barbara
"""

start_text_group = """
Приветсвую всех участников группы {group_name}, 
Добро Пожаловать в SantaBot

Я могу упростить процесс игры в Тайного Санту
"""


help_text = f"""
Я могу помочь вам управлять игрой в Тайного Санту в Telegram. Если вы впервые пользуетесь СантаБотом, ознакомьтесь с правилами /rules .

Вы можете управлять мной, отправив эти команды:

/start - Старт бота в чате 
/help - Список всех команд бота
/faq - Часто Задаваемые вопросы
/rules - Правила игры в Тайного Санту

{hbold("Команды доступные только в группах")}
/show_participants - Показать Список всех Участников чата
/add_participants - Кнопка для участия в игре (Должен быть Админом)
/lets_start_party - Начать Жеребьёвку Участников (Должен быть Админом)
/quit_secret_santa - Остановить Игру (Должен быть Админом)


{hbold("Команды доступные только в личных сообщениях с ботом")}
/update_wish_list - Обновить Список Желаний
/notify_santa - Оповестить своего получателя о готовом подарке
/gift_received - Оповестить Санту что ты получил Подарок

"""

faq_text = f"""
Часто Задаваемые Вопросы 
Игры {hbold("Тайный Санта")}

Что такое игра "Тайна Санта"?

"Тайна Санта" - это игра обмена подарками, где участники тайно дарят подарки друг другу.
"""

rules_text = """
Правила игры в Тайного Санту

Бюджет подарков:
    Обычно заранее устанавливается ограничение по стоимости подарка, чтобы все подарки были примерно одинаковой ценности.

Вручение подарков:
    Подарки обычно вручаются во время совместного мероприятия, например, на корпоративной вечеринке или семейном ужине.
    Подарки можно положить под общую елку или в специально отведённое место, а затем каждый участник находит подарок с его именем.  
    
Покупка и упаковка подарков:
    Участники покупают и упаковывают подарки для того, чьё имя они вытянули.
    Важно сохранять анонимность. Получатель не должен знать, кто его Тайный Санта.

Раскрытие Тайных Сант:
    После того, как все подарки распакованы, можно раскрыть, кто кому дарил подарки, или оставить это в тайне.
"""

emojis = [
    "🎄",   
    "🌲",
    "⛄️",
    "❄️",
    "🎁",
    "☃️",
    "🔥",
    "🌟",
    "🦌",
    "🥳",
    "🎉",
    "🧦",
    "🔔",
    "🎂",
    "🍪",
    "🥛",
    "🕯",
    "🍰",
    "🎆",
    "🍻",
    "🍾",
    "⭐️",
    "✨",
    "🥂",
    "⛸",
    "🛷",
    "🏂",
    "⛷",
    "🎿",
    "🎇",
    "🌠",
    "🎊",
    "🚀",
]

santa_emojis = ["🎅🏻", "🎅🏽", "🤶🏿", "🤶🏾", "🤶🏼", "🎅🏿", "🧑🏿‍🎄", "🧑‍🎄", "🧑🏻‍🎄", "🧑🏽‍🎄"]