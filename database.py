from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123456seven@localhost/fastapi'
# Extrtracting data from config folder
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# ENGINE - connect sqlalchemy(ORM) to postgresql database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This is a factory function provided by SQLAlchemy that creates new session objects. 
# A session object manages the database operations such as querying and persisting data (inserting, updating, deleting).
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
#                             password = '123456seven',cursor_factory = RealDictCursor) # curso..--> for column names
#         cursor = conn.cursor() # cursor -> used to interact with the database, allowing u to execute SQL queries and fetch data
#         print("databse connection was successfull!!")
#         break
#     except Exception as error:
#         print("Connecting to database failed & the error is -> ", error)
#         time.sleep(2)