from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI

db = Gino()


async def open_db():
    # Устанавливаем связь с базой данных
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

async def create_db():
    # Создаем таблицы
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    #await db.gino.drop_all()
    await db.gino.create_all()
    await db.pop_bind().close()

async def drop_db():
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.pop_bind().close()

async def close_db():
    await db.pop_bind().close()




