from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, Date, DateTime, Time, ForeignKey)
from sqlalchemy import sql
from utils.db_api.database import db

# Создаем класс таблицы со списком пользователей
# 1. Emo_users имеет графы (графы last_name и sur_name предлагаю удалить):
# * user_id – цифра – id пользователя, взятое из его УЗ телеграмм;
# * first_name – строка – первое имя пользователя, взятое из его УЗ телеграмм;
# * name – строка – имя пользователя, указанное в диалоге с ботом;
# * StartTime – цифра – час начала опроса;
# * EndTime – цифра – час завершения опроса;
# * TaskTime – цифра – час начала задачи «на прокачку»;
# * ZoneTime – цифра – временная зона пользователя; ?м.б. лишняя?
# * Period – цифра – промежуток времени в часах между опросами;
# * PrevData – цифра – календарное число дня, запомненное при наступлении начала опроса (служит для расчета номера текущего дня работы); ?м.б. лишняя?
# * CurrentDay – цифра – номер текущего дня работы (служит для вызова соответствующей ему задачи «на прокачку»);
# * RunTask – цифра – флажок запуска задания;
# * RunPoll – цифра – флажок запуска опроса;
# * Stage – цифра – номер стадии (четырехзначное число, где: старшие 2 знака № стадии, младшие 2 знака № этапа; служит для вызова соответствующей обработки ответа пользователя);
#
class Emo_users(db.Model):
    __tablename__ = 'emo_users'
    query: sql.Select
    # Уникальный идентификатор
    user_id = Column(BigInteger, primary_key=True, unique=True)
    first_name = Column(String(20))
    name = Column(String(20))
    StartTime = Column(Integer)
    EndTime = Column(Integer)
    ZoneTime = Column(Integer)
    Period = Column(Integer)
    CurrentDay = Column(Integer)
    def __repr__(self):
        return "{}<{}>".format(self.name, self.user_id)

# 2. Emotions имеет графы:
# * user_id – цифра – id пользователя, взятое из его УЗ телеграмм;
# * fix_date – ?строка? – дата ответа пользователя;
# * fix_time –  ?строка? – время ответа пользователя;
# * emotion – цифра – ответ пользователя в виде индекса из списка эмоций;
#
class Emotions(db.Model):
    __tablename__ = 'emotions'
    query: sql.Select
    user_id = Column(BigInteger)
    fix_date = Column(Date)
    fix_time = Column(Time)
    emotion = Column(String(20))
    reason =  Column(String(50))
    fk = db.ForeignKeyConstraint(['user_id'], ['emo_users.user_id'], name="fk")
    def __repr__(self):
        return "{}<{}>".format(self.user_id, self.emotion)

# 2. Tasks имеет графы:
# * user_id – цифра – id пользователя, взятое из его УЗ телеграмм;
# * task_number – цифра – значение равное значению CurrentDay на момент вызова задачи;
# * fix_date – ?строка? – дата ответа пользователя;
# * fix_time – ?строка? – время ответа пользователя;
# * answer – строка – ответ пользователя (записывается в необработанном виде с ограничением на ?50? символов)
class Tasks(db.Model):
    __tablename__ = 'tasks'
    query: sql.Select
    user_id = Column(BigInteger)
    fix_date = Column(Date)
    fix_time = Column(Time)
    task_number = Column(Integer)
    answer = Column(String(100))
    fk2 = db.ForeignKeyConstraint(['user_id'], ['emo_users.user_id'], name="fk2")
    def __repr__(self):
        return "{}<{}>".format(self.user_id, self.answer)
