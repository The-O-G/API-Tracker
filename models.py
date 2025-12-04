from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the connection string from the environment variable
conn_string = os.getenv("DATABASE_URL")


Base = declarative_base()

class URLList(Base):
    __tablename__ = "url_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    has_filter = Column(Boolean, default=False)
    filter = Column(String, nullable=True)

    def __repr__(self):
        return f"<URLList(id={self.id}, url={self.url}, is_active={self.is_active}, has_filter={self.has_filter})>"

# from sqlalchemy import create_engine

# engine = create_engine(conn_string)
# Base.metadata.create_all(engine)
