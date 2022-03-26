from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  
from .config import settings

# engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
engine = create_engine(f'mysql+pymysql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'%quote(settings.database_password))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)
Base = declarative_base()
conn = engine.connect()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# database connection started-----------------------------------------------------------------------------------
# import mysql.connector
# while True:
#     try:
#         mydb = mysql.connector.connect(
#             host="localhost", user="ucifer", password="Ucifer@123",database="fast"
#         )
#         mycursor = mydb.cursor(dictionary=True)
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error:",error)
#         time.sleep(2)
# # database connection ended------------------------------------------------------------------------------------------
