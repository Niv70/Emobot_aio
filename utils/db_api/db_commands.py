from typing import List

from sqlalchemy import and_

from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.database import db


#

loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
