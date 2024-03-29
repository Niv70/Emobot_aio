import datetime
import logging
import pandas as pd
import sqlalchemy
from aiogram.dispatcher import FSMContext
from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, Date, DateTime, Time, ForeignKey, desc)
from sqlalchemy import sql, func, create_engine
from gino import Gino

from data.config import POSTGRES_URI
from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.database import db
from loader import LAST_DAY
# не удалять !!!
import psycopg2
import xlsxwriter


async def db_add_user(user_id, first_name, name, start_time=8, period=2, end_time=17, zone_time=7, current_day=0,
                      task_time=99, last_day=LAST_DAY):
    item: Emo_users
    item = await Emo_users.create(user_id=user_id, first_name=first_name, name=name, StartTime=start_time,
                                  EndTime=end_time, ZoneTime=zone_time, Period=period, CurrentDay=current_day,
                                  TaskTime=task_time, LastDay=last_day)
    return item


async def db_update_user_settings(user_id, name="None", start_time=8, period=2, end_time=17, zone_time=7, current_day=0,
                                  task_time=99, last_day=LAST_DAY):
    item: Emo_users
    item = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    await item.update(user_id=user_id, name=name, StartTime=start_time,
                      EndTime=end_time, ZoneTime=zone_time, Period=period, CurrentDay=current_day,
                      TaskTime=task_time, LastDay=last_day).apply()
    return item


async def db_update_current_day(user_id, current_day=0):
    item: Emo_users
    item = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    await item.update(user_id=user_id, CurrentDay=current_day).apply()
    return item


async def db_update_last_day(user_id, last_day=0):
    item: Emo_users
    item = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    await item.update(user_id=user_id, LastDay=last_day).apply()
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


# lastEmotions = None


async def db_save_emotions(user_id, emotion, state: FSMContext):
    # global lastEmotions
    # lastEmotions = emotion
    data = await state.get_data()
    await state.update_data(emotion=emotion)


async def db_save_reason(user_id, reason, state: FSMContext):
    # global lastEmotions
    data = await state.get_data()
    emotion = data.get("emotion")
    tmz = data.get("tmz")
    c_data = datetime.datetime.now() + datetime.timedelta(hours=tmz)
    await Emotions.create(user_id=user_id, fix_date=c_data.date(),
                          fix_time=c_data.time(), emotion=emotion, reason=reason)


# task_number = Column(Integer)
async def db_save_task(user_id, task_number, answer):
    item: Tasks  # здесь учет часового пояса не делал (очень много вызовов функции) - обработки ее значений пока нет
    item = await Tasks.create(user_id=user_id, fix_date=datetime.datetime.now().date(),
                              fix_time=datetime.datetime.now().time(), task_number=task_number, answer=answer[:100])
    return item


async def stat_five_emotions(user_id):
    stats = await db.select([Emotions.emotion, func.count(Emotions.emotion), ]).select_from(Emotions).group_by(
        Emotions.emotion).order_by(desc(func.count(Emotions.emotion))).where(Emotions.user_id == user_id).limit(
        5).gino.all()
    str_stats = "<pre>Самые часто испытываемые эмоции\n" \
                "===============================\n"
    for i in stats:
        str_stats += "{0:20s} : {1:3d}\n".format(i[0], i[1])
    str_stats += "</pre>"
    return str_stats


async def upload_xls(user_id):
    engine0 = create_engine(POSTGRES_URI)
    sf = pd.read_sql("SELECT public.emotions.fix_date AS Дата, public.emotions.fix_time AS Время,"
                     "public.emotions.emotion AS Эмоция, public.emotions.reason AS Причина FROM public.emotions WHERE public.emotions.user_id={0}".format(user_id),engine0)
    writer = pd.ExcelWriter("./Emotions-{0}.xlsx".format(user_id), engine='xlsxwriter', date_format="dd-mm-yyyy",
                            datetime_format="hh:mm")
    sf.to_excel(writer, sheet_name="Реестр эмоций")
    writer.save()
    return "./Emotions-{0}.xlsx".format(user_id)
