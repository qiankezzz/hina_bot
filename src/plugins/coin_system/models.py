# coding:utf-8
import asyncio

from pathlib import Path
from .config import driver, log_debug, log_info

from databases import Database, DatabaseURL
from sqlalchemy import Column, Integer, String, Sequence, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_PATH = Path() / 'data' / 'coin_system' / 'coin.system.db'
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

database = Database(DatabaseURL(f"sqlite:///{DATABASE_PATH}"))
engine = create_engine(str(database.url))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('person_id_seq'), primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    group_id = Column(Integer)
    nickname = Column(String)
    coins = Column(Integer, default=20)

    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='user_group_unique'),
    )


async def get_db() -> SessionLocal:
    session = SessionLocal()
    return session


async def init_db():
    await database.connect()
    Base.metadata.create_all(bind=engine)


async def close_db():
    await database.disconnect()


async def get_user(user_id: int, group_id: int) -> User:
    async with database:
        db = await get_db()
        return db.query(User).filter(User.user_id == user_id, User.group_id == group_id).first()


async def get_user_coins(user_id: int, group_id: int) -> int:
    user = await get_user(user_id, group_id)
    return user.coins if user else -1


async def add_user(user_id: int, group_id: int, nickname: str):
    user = await get_user(user_id, group_id)
    if user:
        return 1
    async with database:
        db = await get_db()
        db.add(User(user_id=user_id, group_id=group_id, nickname=nickname))
        db.commit()


async def add_user_coins(user_id: int, group_id: int, coins_to_add: int):
    user = await get_user(user_id, group_id)
    if not user:
        return 1

    async with database:
        db = await get_db()
        user = db.query(User).filter(User.user_id == user_id, User.group_id == group_id).first()
        user.coins += coins_to_add
        db.commit()


async def reduce_user_coins(user_id: int, group_id: int, coins_to_reduce: int):
    user = await get_user(user_id, group_id)
    if not user:
        return

    async with database:
        db = await get_db()
        user = db.query(User).filter(User.user_id == user_id, User.group_id == group_id).first()
        user.coins -= coins_to_reduce
        db.commit()


async def set_user_coins(user_id: int, group_id: int, coins: int):
    user = await get_user(user_id, group_id)
    if not user:
        return

    async with database:
        db = await get_db()
        user = db.query(User).filter(User.user_id == user_id, User.group_id == group_id).first()
        user.coins = coins
        db.commit()


async def get_user_nickname(user_id: int, group_id: int) -> str:
    user = await get_user(user_id, group_id)
    return user.nickname if user else ''


async def get_all_users() -> list[User]:
    async with database:
        db = await get_db()
        return await db.query(User).all()


async def get_all_group_id() -> list[int]:
    async with database:
        db = await get_db()
        return await db.query(User.group_id).distinct().all()


@driver.on_startup
async def startup():
    try:
        await init_db()

        log_info('coin_system', '数据库连接<g>成功</g>')
    except Exception as e:
        log_debug('coin_system', f'数据库连接<r>失败，{e}</r>')
        raise e


@driver.on_shutdown
async def shutdown():
    await close_db()
    log_info('coin_system', '数据库断开连接<g>成功</g>')


async def test():
    await init_db()
    print("success")
    await close_db()


if __name__ == '__main__':
    asyncio.run(test())
