from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.reader import Reader
from app.db.schemas.reader import ReaderCreate, ReaderUpdate
from sqlalchemy.exc import NoResultFound, IntegrityError


async def get_readers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Reader).offset(skip).limit(limit))
    return result.scalars().all()


async def create_reader(db, reader_data):
    new_reader = Reader(
        email=reader_data.email,
        name=reader_data.name
    )
    db.add(new_reader)
    await db.commit()
    await db.refresh(new_reader)
    return new_reader


async def get_reader(db, reader_id):
    result = await db.execute(select(Reader).where(Reader.id == reader_id))
    reader = result.scalars().first()
    if not reader:
        raise NoResultFound(f"Читатель с id:{reader_id} не найден")
    return reader


async def update_reader(db, reader_id, reader_data):
    result = await db.execute(select(Reader).where(Reader.id == reader_id))
    reader = result.scalars().first()
    if not reader:
        raise NoResultFound(f"Читатель с id:{reader_id} не найден")
    if reader_data.name is not None:
        reader.name = reader_data.name
    if reader_data.email is not None:
        reader.email = reader_data.email
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Читатель с таким email уже существует")
    await db.refresh(reader)
    return reader


async def delete_reader(db, reader_id):
    result = await db.execute(select(Reader).where(Reader.id == reader_id))
    reader = result.scalars().first()
    if not reader:
        raise NoResultFound(f"Читатель с таким id:{reader_id} не существует")
    await db.delete(reader)
    await db.commit()
    return reader
