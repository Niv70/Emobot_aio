import datetime
import logging

import sqlalchemy
from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, Date, DateTime, Time, ForeignKey)
from sqlalchemy import sql
from gino import Gino

from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.database import db

Possible_Emotions = ['злость', 'трепет', 'угрюмость', 'отчужденность',
                     'гнев', 'обеспокоенность ', 'серьезность', 'неловкость',
                     'возмущение', 'испуг', 'подавленность', 'удивление',
                     'ненависть', 'тревога', 'разочарование', 'шок',
                     'обида', 'волнение', 'боль', 'поражение',
                     'сердитость', 'боязнь', 'застенчивость', 'остолбенение',
                     'досада', 'ужас', 'покинутость', 'изумление',
                     'раздражение', 'ощущение угрозы', 'удрученность', 'потрясение',
                     'оскорбленность', 'ошеломленность', 'усталость', 'энтузиазм',
                     'воинственность', 'опасение', 'глупость', 'восторг',
                     'бунтарство', 'уныние', 'апатия', 'возбужденность',
                     'сопротивление', 'ощущение тупика', 'самодовольство', 'страсть',
                     'зависть', 'запутанность', 'скука', 'эйфория',
                     'надменность', 'потерянность', 'истощение', 'трепет',
                     'презрение', 'дезориентация', 'расстройство', 'решимость',
                     'отвращение', 'бессвязность', 'упадок сил', 'дерзость',
                     'подавленность', 'одиночество', 'нетерпеливость', 'удовлетворенность',
                     'уязвленность', 'изолированность', 'вспыльчивость', 'гордость',
                     'подозрительноость', 'грусть', 'тоска', 'сентиментальность',
                     'настороженность', 'печаль', 'стыд', 'счастье',
                     'озабоченность', 'горе', 'вина', 'радость',
                     'тревожность', 'угнетенность', 'униженность', 'блаженство',
                     'страх', 'мрачность', 'ущемленность', 'забавность',
                     'нервозность', 'отчаяние', 'смущение', 'восхищение',
                     'ожидание', 'опустошенность', 'неудобство', 'триумф',
                     'взволнованность', 'беспомощность', 'тяжесть', 'удовольствие',
                     'слабость', 'сожаление', 'мечтательность',
                     'ранимость', 'скорбь', 'очарование',
                     'неудовольствие', 'растерянность ', 'принятие']


async def db_add_user(user_id, first_name, name):
    item: Emo_users
    item = await Emo_users.create(user_id=user_id, first_name=first_name, name=name)
    return item


async def get_name_by_item(user_id):
    item: Emo_users = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    if item is None:
        return None
    else:
        return item.name


lastEmotions = None


async def db_save_emotions(user_id, emotion):
    global lastEmotions
    lastEmotions = await Emotions.create(user_id=user_id, fix_date=datetime.datetime.now().date(),
                                         fix_time=datetime.datetime.now().time(), emotion=emotion)


async def db_save_reason(reason):
    global lastEmotions
    await lastEmotions.update(reason=reason).apply()

#task_number = Column(Integer)
async def db_save_task(user_id, task_number, answer):
    item: Tasks
    item = await Tasks.create(user_id=user_id, fix_date=datetime.datetime.now().date(),
                        fix_time=datetime.datetime.now().time(), task_number=task_number, answer=answer)
    return item
