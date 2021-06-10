import datetime
import logging

import sqlalchemy
from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, Date, DateTime, Time, ForeignKey)
from sqlalchemy import sql
from gino import Gino

from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.database import db

Possible_Emotions = ['злость',	'трепет',	'угрюмость',	'отчужденность',
'гнев',	'обеспокоенность ',	'серьезность',	'неловкость',
'возмущение',	'испуг',	'подавленность',	'удивление',
'ненависть',	'тревога',	'разочарование',	'шок',
'обида',	'волнение',	'боль',	'поражение',
'сердитость',	'боязнь',	'застенчивость',	'остолбенение',
'досада',	'ужас',	'покинутость',	'изумление',
'раздражение',	'ощущение угрозы',	'удрученность',	'потрясение',
'оскорбленность',	'ошеломленность',	'усталость',	'энтузиазм',
'воинственность',	'опасение',	'глупость',	'восторг',
'бунтарство',	'уныние',	'апатия',	'возбужденность',
'сопротивление',	'ощущение тупика',	'самодовольство',	'страсть',
'зависть',	'запутанность',	'скука',	'эйфория',
'надменность',	'потерянность',	'истощение',	'трепет',
'презрение',	'дезориентация',	'расстройство',	'решимость',
'отвращение',	'бессвязность',	'упадок сил',	'дерзость',
'подавленность',	'одиночество',	'нетерпеливость',	'удовлетворенность',
'уязвленность',	'изолированность',	'вспыльчивость',	'гордость',
'подозрительноость',	'грусть',	'тоска',	'сентиментальность',
'настороженность',	'печаль',	'стыд',	'счастье',
'озабоченность',	'горе',	'вина',	'радость',
'тревожность',	'угнетенность',	'униженность',	'блаженство',
'страх',	'мрачность',	'ущемленность',	'забавность',
'нервозность',	'отчаяние',	'смущение',	'восхищение',
'ожидание',	'опустошенность',	'неудобство',	'триумф',
'взволнованность',	'беспомощность',	'тяжесть',	'удовольствие',
'слабость',	'сожаление',	'мечтательность',
'ранимость',	'скорбь',	'очарование',
'неудовольствие',	'растерянность ',	'принятие']


async def db_add_user(user_id, first_name, name):
    item: Emo_users
    return item.create(user_id=user_id, first_name=first_name, name=name)

async def get_name_by_item(user_id):
    item: Emo_users = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    if item is None:
        return None
    else:
        return item.name

async def db_save_emotions(user_id, emotion):
    item: Emotions
    item.user_id = user_id
    item.fix_date = datetime.datetime.now().date()
    item.fix_time = datetime.datetime.now().time()
    item.emotion = emotion
    return item.create()

async def db_save_reason(user_id, reason):
    item: Emotions
    item.user_id = user_id
    item.fix_date = datetime.datetime.now().date()
    item.fix_date = datetime.datetime.now().date()
    item.reason = reason
    return item.create()

async def db_save_task(user_id, task_number, answer):
    item: Tasks
    item.user_id = user_id
    item.fix_date = datetime.datetime.now().date()
    item.fix_date = datetime.datetime.now().date()
    item.query = task_number
    item.answer = answer
    return item.create()