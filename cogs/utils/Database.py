from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_databases import Base
import os

class Database:
    def __init__(self):
        os.environ.get('DB_HOST')
        engine = create_engine(f"mysql+pymysql://{os.environ.get('DB_USERNAME')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_DATABASE')}?charset=utf8mb4", echo=True)
        print(engine.table_names())
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    async def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(str(e))
