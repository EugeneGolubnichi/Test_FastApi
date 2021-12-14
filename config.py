
"""Данные для входа в Постгрес БД"""
#database='horse_db'
#user='horse',
#password = 'horse',
#host="127.0.0.1"
DATABASE_URL = "postgresql+psycopg2://horse:horse@localhost/horse_db"
REDIS_URL = "redis://localhost/0"


#Base = declarative_base()
#engine = create_engine("postgresql+psycopg2://horse:horse@localhost/horse_db")