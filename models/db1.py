import os
from typing import Type, List, TypeVar

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, Field, Session, select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from tools import LanguageSingleton

T = TypeVar("T")


class ChapterFileX(SQLModel, table=True):
    url: str = Field(primary_key=True)
    file_id: str
    file_unique_id: str
    cbz_id: str
    cbz_unique_id: str
    telegraph_url: str


class DBX(metaclass=LanguageSingleton):
    
    def __init__(self, dbname: str = 'sqlite:///test.db'):
        if dbnamex.startswith('postgres://'):
            dbnamex = dbnamex.replace('postgres://', 'postgresql+asyncpg://', 1)
        if dbnamex.startswith('sqlite'):
            dbnamex = dbnamex.replace('sqlite', 'sqlite+aiosqlite', 1)
    
        self.engine = create_async_engine(dbnamex)
        
    async def connect(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all, checkfirst=True)

    async def add(self, other: SQLModel):
        async with AsyncSession(self.engine) as session:  # type: AsyncSession
            async with session.begin():
                session.add(other)

    async def get(self, table: Type[T], id) -> T:
        async with AsyncSession(self.engine) as session:  # type: AsyncSession
            return await session.get(table, id)

    async def erase(self, other: SQLModel):
        async with AsyncSession(self.engine) as session:  # type: AsyncSession
            async with session.begin():
                await session.delete(other)

    async def get_chapter_file_by_id(self, id: str):
        async with AsyncSession(self.engine) as session:  # type: AsyncSession
            statement = select(ChapterFile).where((ChapterFile.file_unique_id == id) |
                                                  (ChapterFile.cbz_unique_id == id) |
                                                  (ChapterFile.telegraph_url == id))
            return (await session.exec(statement=statement)).first()
