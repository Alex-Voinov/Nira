from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from .db import async_session


class Base(DeclarativeBase):
    
    @classmethod
    async def create(cls, **kwargs):
        """
        Создаёт новую запись в базе.
        Пример:
            await User.create(name="Egor", age=16)
        Параметры:
            **kwargs - ключи должны соответствовать полям модели (User, Product и т.д.)
        """
        async with async_session() as session:
            obj = cls(**kwargs)               
            session.add(obj)                  
            await session.commit()            
            return obj                        

    @classmethod
    async def find_by(cls, column: str, value):
        """
        Универсальный поиск по значению одного поля.
        Пример:
            await User.find_by("name", "Egor")
        Параметры:
            column - имя поля модели (например, "name", "age")
            value  - значение, по которому ищем
        Возвращает список объектов модели, удовлетворяющих условию.
        """
        async with async_session() as session:
            col = getattr(cls, column)  
            stmt = select(cls).where(col == value)
            result = await session.execute(stmt)  
            return result.scalars().all()         

    @classmethod
    async def find_all(cls):
        """
        Получить все записи из таблицы модели.
        Пример:
            await User.find_all()
        Возвращает список всех объектов модели.
        """
        async with async_session() as session:
            result = await session.execute(select(cls))
            return result.scalars().all()              

    @classmethod
    async def find_by_id(cls, id_: int):
        """
        Найти запись по первичному ключу.
        Пример:
            await User.find_by_id(1)
        """
        async with async_session() as session:
            return await session.get(cls, id_) 

    @classmethod
    async def update(cls, id_: int, **kwargs):
        """
        Обновить запись по первичному ключу.
        Пример:
            await User.update(1, name="Alex")
        Параметры:
            id_ - первичный ключ
            **kwargs - поля и новые значения
        """
        async with async_session() as session:
            obj = await session.get(cls, id_)   
            for key, value in kwargs.items():
                setattr(obj, key, value)        
            await session.commit()              
            return obj                          

    @classmethod
    async def delete(cls, id_: int):
        """
        Удалить запись по первичному ключу.
        Пример:
            await User.delete(1)
        """
        async with async_session() as session:
            obj = await session.get(cls, id_)
            await session.delete(obj)         
            await session.commit()       
