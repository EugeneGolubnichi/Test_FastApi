import random
import asyncpg
from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from anogram import is_input_anogram
import aioredis
from mac_creator import device_creator, mac_creator
from models import add_endpoints, add_10_devices, Device
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL, REDIS_URL


app = FastAPI()

# создаю и заполняю таблицу endpoints при запуске сервера
add_endpoints()


@app.get("/")
async def root():
    return {"message": 'функции PostgreSQL и SQLAlchemy написал не в асинхронном режиме.'
                       ' Успел разобраться только с aioredis и fastapi. '
                       'try/exept/finally - тоже не успел обернуть.'
                       ' Все функции по заданию работают.'
                       'Спасибо за возможность!'}


@app.get("/isanogram")
async def counter_of_anagrams(q: str = Query(None), q2: str = Query(None)):
    """ Принимает на вход две строки.
     Возвращает количество полученных анаграмм за все время."""
    is_anagram = is_input_anogram(q, q2)

    return await counter(is_anagram)

async def counter(is_anagram: bool):
    """ функция увеличения счетчика. на вход приходит тру/фолс"""
    redis = aioredis.from_url(REDIS_URL)
    # идем в редис за счетчиком
    my_counter_of_anagrams = await redis.get("counter")
    # интуем
    my_counter_of_anagrams = int(my_counter_of_anagrams)
    # если значения не получили считаем что наш счетчик = 0

    if not my_counter_of_anagrams:          # эквивалентно if ...== None
        my_counter_of_anagrams = 0
        # записываем его в редис
        await redis.set("counter", my_counter_of_anagrams)

    # если на вход пришло тру - увеличиваем счетчик на 1
    # если фолс - оставляем таким же
    if is_anagram:  # эквивалентно    if is_anagram == True
        result = 'Yes, it is anagrmm '
        my_counter_of_anagrams = my_counter_of_anagrams + 1
    else:
        result = 'Not an anagrmm '
        my_counter_of_anagrams = my_counter_of_anagrams
    # записываем в редис актуальное значение счетчика
    await redis.set("counter", my_counter_of_anagrams)
    # возвращаем значение, которе потом выведется в браузере
    return f"{result}. Total counter of anagrams: {my_counter_of_anagrams}"


@app.get("/device_add", status_code=201)
def add_10_devices():
    """Добавляет в таблицу device 10 записей, возвращает HTTP код состояния"""
    #ВЫНЕСТИ ОТДЕЛЬНО
    Base = declarative_base()
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    # создаем список endpoint'ов
    list_of_endpoints = [None, 1, 2]
    # добавляем 10 записей
    for i in range(10):
        d1 = Device(
            dev_id=mac_creator(),
            dev_type=device_creator(),
            endpoint=random.choice(list_of_endpoints)
                   )
        session.add(d1)
        session.commit()
        session.close()

    return JSONResponse(status_code=status.HTTP_201_CREATED,content=status.HTTP_201_CREATED)




@app.get('/get_list_of_devices')
def query_set():
    """Функция выбирает девайсы из таблицы devices без endpoint и возвращает их"""
    #ВЫНЕСТИ ОТДЕЛЬНО
    Base = declarative_base()
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    # создаем запрос
    query_list = session.query(Device.id, Device.dev_id, Device.dev_type, ).filter_by(endpoint = None).all()

    return query_list

@app.get('/count_of_devices_without_endpoints')
def query_amount():
    """Функция возвращает количество устройств без endpoint, сгруппированное по их типам"""
    #УБРАТЬ ОТДЕЛЬНО
    Base = declarative_base()
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    # формируем запрос
    query_count = session.query(Device.dev_type, func.count(Device.dev_type)).filter_by(endpoint=None).group_by(
        Device.dev_type)
    return query_count



