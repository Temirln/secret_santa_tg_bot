from aiogram.utils.markdown import hbold

START_TEXT_PRIVATE = """
О-хо-хо!

Приветствую <b>{user_name}</b>, 
Добро Пожаловать в Телеграм Бота 
<b>Secret Santa Barbara</b>

Я помогу тебе организовать игру в Тайного Санту прямо в группе Телеграм, все что тебе нужно это добавить меня в свою группу 

Можешь ознакомиться с командами бота /help и правилой игры в Тайного Санту с помощью бота /rules

Если есть вопросы, пожелания и предложения, пишите -> @toleubekov_temirlan
"""

START_TEXT_GROUP = """
Приветствую всех участников группы {group_name}, Добро Пожаловать в SantaBot. 

Я помогу вам упростить процесс игры в Тайного Санту внутри группы

Если вы впервые пользуетесь ботом советуем ознакомиться с правилами через команду /rules и ознакомиться со всеми командами бота /help.

"""


HELP_TEXT = f"""
Я могу помочь вам управлять игрой в Тайного Санту в Telegram. Если вы впервые пользуетесь СантаБотом, ознакомьтесь с правилами \n/rules

Вы можете управлять мной, отправив эти команды:

/start - Старт бота в чате 
/help - Список всех команд бота
/faq - Часто Задаваемые вопросы
/rules - Правила игры в Тайного Санту

{hbold("Команды доступные только в группах")}
/all - Упомянуть всех в чате
/show_participants - Показать Участников игры
/add_participants - Кнопка для участия в игре (Должен быть Админом)
/lets_start_party - Начать Распределение Участников (Должен быть Админом)
/restart_secret_santa - Перезапустить Игру для Группы (Должен быть Админом)


{hbold("Команды доступные только в личных сообщениях с ботом")}
/update_wish_list - Обновить Список Желаний
/notify_santa - Оповестить своего получателя о готовом подарке
"""

FAQ_TEXT = """
Часто Задаваемые Вопросы 

Санта решил ответить на часто задаваемые вопросы. С каждым днем задаются одни и те же вопросы. А именно:

1) Что такое игра "Тайна Санта"?

"Тайна Санта" - это игра обмена подарками, где участники тайно дарят подарки друг другу.


2) Могу ли я добавить бота в несколько групп?

Да вы можете участвовать в игре в нескольких группах и это никак не отразится на текущую игру


3) Могу ли я добавить нового участника в игру с уже распределенной Жеребъёвкой?

Никак нет, вам придется сперва завершить текущую игру или перезапустить ее


4) Как расчитывается распределение участников?

Сперва каждому участнику присваивается определенный неповторящийся номер, после производится деление с остатком номера каждого участника на количество участников. В резултьтате деления выходит номер другого участника, он и будет его Сантой.
"""

RULES_TEXT = """
Правила игры в Тайного Санту в Телеграм боте Secret Santa Barbara

1)  Сперва вам нужно будет добавить бота в вашу телеграм группу и выдать ему разрешения на чтение и отправку сообщении

2)  С помощью команды /add_participants создаете кнопку для Добавления Участников, где участники группы могут решить участвовать им или нет

3)  После того как достаточное количество участников собрано, командой /lets_start_party запускаете распределение, каждому участнику в личное сообщение придет имя кому он будет дарить подарок

4)  Каждый участник может добавить список желании который хотел(а) бы получить в качестве подарка и Тайный Санта уже может сам выбрать что дарить его получателю 

5)  Покупка и упаковка подарков:
Участники покупают и упаковывают подарки для того, чьё имя они вытянули.
Важно сохранять анонимность. Получатель не должен знать, ни в коем случае не раскрывайте кто его Тайный Санта.

6)  Вручение подарков:
Подарки обычно вручаются во время совместного мероприятия, например, на корпоративной вечеринке или семейном ужине.
Подарки можно положить под общую елку или в специально отведённое место, а затем каждый участник находит подарок с его именем.  
    
Раскрытие Тайных Сант:

После того, как все подарки распакованы, можно раскрыть, кто кому дарил подарки, или оставить это в тайне.
"""

EMOJIS = [
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

SANTA_EMOJIS = ["🎅🏻", "🎅🏽", "🤶🏿", "🤶🏾", "🤶🏼", "🎅🏿", "🧑🏿‍🎄", "🧑‍🎄", "🧑🏻‍🎄", "🧑🏽‍🎄"]
