import os

from sqlalchemy import Column, String, Integer, Boolean, BIGINT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StarBoardSettings(Base):
    __tablename__ = 'starboard_settings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT)
    enabled = Column(Boolean, default=False)
    channel_id = Column(BIGINT, nullable=False)
    emoji = Column(String(255), nullable=False)
    threshold = Column(Integer, nullable=False)


class StarBoardIgnoredChannels(Base):
    __tablename__ = 'starboard_ignored_channels'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT)
    channel_id = Column(BIGINT, nullable=False)


class StarBoardMessages(Base):
    __tablename__ = 'starboard_messages'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT)
    starboard_message_id = Column(BIGINT)
    original_message_id = Column(BIGINT)
    count = Column(Integer)


class StarboardAllowedRoles(Base):
    __tablename__ = 'starbaord_roles'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT)
    role_id = Column(BIGINT)


if __name__ == '__main__':
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine(
        f"mysql+pymysql://{os.environ.get('DB_USERNAME')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_DATABASE')}?charset=utf8mb4",
        echo=True)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(bind=engine)
    print("Done!")
