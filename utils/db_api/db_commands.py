import datetime
import logging

import sqlalchemy
from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, Date, DateTime, Time, ForeignKey, desc)
from sqlalchemy import sql, func
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


async def db_add_user(user_id, first_name, name, start_time=8, period=2, end_time=17, zone_time=7, current_day=0,
                      task_time=99):
    item: Emo_users
    item = await Emo_users.create(user_id=user_id, first_name=first_name, name=name, StartTime=start_time,
                                  EndTime=end_time, ZoneTime=zone_time, Period=period, CurrentDay=current_day,
                                  TaskTime=task_time)
    return item


async def db_update_user_settings(user_id, name="None", start_time=8, period=2, end_time=17, zone_time=7, current_day=0,
                                  task_time=99):
    item: Emo_users
    item = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    await item.update(user_id=user_id, name=name, StartTime=start_time,
                      EndTime=end_time, ZoneTime=zone_time, Period=period, CurrentDay=current_day,
                      TaskTime=task_time).apply()
    return item


async def get_name_by_id(user_id):
    item: Emo_users = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    if item is None:
        return None
    else:
        return item.name


async def get_settings_by_id(user_id):
    item: Emo_users = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    if item is None:
        return None
    else:
        return item


lastEmotions = None


async def db_save_emotions(user_id, emotion):
    global lastEmotions
    lastEmotions = emotion


async def db_save_reason(user_id, reason):
    global lastEmotions
    await Emotions.create(user_id=user_id, fix_date=datetime.datetime.now().date(),
                          fix_time=datetime.datetime.now().time(), emotion=lastEmotions, reason=reason)


# task_number = Column(Integer)
async def db_save_task(user_id, task_number, answer):
    item: Tasks
    item = await Tasks.create(user_id=user_id, fix_date=datetime.datetime.now().date(),
                              fix_time=datetime.datetime.now().time(), task_number=task_number, answer=answer)
    return item


async def stat_five_emotions(user_id):
    stats = await db.select([Emotions.emotion, func.count(Emotions.emotion), ]).select_from(Emotions).group_by(
        Emotions.emotion).order_by(desc(func.count(Emotions.emotion))).where(Emotions.user_id == user_id).limit(
        5).gino.all()
    str_stats = " Самые часто испытываемые эмоции\n" \
                "==================================\n"
    for i in stats:
        str_stats += "{0:20s} : {1:3d}\n".format(i[0], i[1])
    return str_stats
