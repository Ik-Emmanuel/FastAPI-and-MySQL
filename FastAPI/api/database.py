from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

with open ('vars.json', 'r') as variables:
    env_vars = json.loads(variables.read())  

# SQLALCHEMY_DATABASE_URL = "mysql://<dbuser>:<dbuserpassword>@/locahost or server /<dbname>"
SQLALCHEMY_DATABASE_URL = f"{env_vars['DB']}://{env_vars['DB_USER']}:{env_vars['DB_PASSWORD']}@localhost/fastapiasync"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# for sqlite: create_engine(SQLALCHEMY_DATABASE_URL , connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
