from gino import Gino, create_engine
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI

db = Gino()

async def open_db():
    global engine0
    # Устанавливаем связь с базой данных
    #engine0 = await create_engine(POSTGRES_URI)
    #db.bind = engine0
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor


async def create_db():
    # Создаем таблицы
    await db.gino.create_all()


async def drop_db():
    await db.gino.drop_all()


async def close_db():
    await db.pop_bind().close()
