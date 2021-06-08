from typing import List

import sqlalchemy
from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, Date, DateTime, Time, ForeignKey)
from sqlalchemy import sql
from gino import Gino

from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.database import db


async def add_user(user_id, first_name, name):
    item: Emo_users
    item.user_id = user_id
    item.first_name = first_name
    item.name = name
    return item.create()

async def get_name_by_item(user_id):
    item0: Emo_users = await Emo_users.query.where(Emo_users.user_id == user_id).gino.first()
    return item0.name
