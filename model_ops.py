from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import URLList, Base
import os
from dotenv import load_dotenv

load_dotenv()


class Model_Operations:
    def __init__(self):
        self.conn_string = os.getenv("DATABASE_URL")
        self.engine = create_engine(self.conn_string)
        self.db = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    # -----------------------------------------------------------
    # CREATE
    # -----------------------------------------------------------
    def create_url(self, name: str, url: str, is_active=True, has_filter=False, filter_value=None):
        session = self.db()
        try:
            new_url = URLList(
                name=name,
                url=url,
                is_active=is_active,
                has_filter=has_filter,
                filter=filter_value,
            )

            session.add(new_url)
            session.commit()
            session.refresh(new_url)
            return new_url
        finally:
            session.close()

    # -----------------------------------------------------------
    # READ (single)
    # -----------------------------------------------------------
    def get_url(self, url_id: int):
        session = self.db()
        try:
            return session.query(URLList).filter(URLList.id == url_id).first()
        finally:
            session.close()

    # -----------------------------------------------------------
    # READ (all)
    # -----------------------------------------------------------
    def get_all_urls(self):
        session = self.db()
        try:
            return session.query(URLList).all()
        finally:
            session.close()

    # -----------------------------------------------------------
    # READ (all)
    # -----------------------------------------------------------
    def get_all_active_urls(self):
        session = self.db()
        try:
            return session.query(URLList).filter(URLList.is_active == True).all()
        
        finally:
            session.close()            

    # -----------------------------------------------------------
    # UPDATE
    # -----------------------------------------------------------
    def update_url(self, url_id: int, **kwargs):
        """
        Example calls:
        update_url(3, name="New Name")
        update_url(3, is_active=False, filter="news")
        """
        session = self.db()
        try:
            item = session.query(URLList).filter(URLList.id == url_id).first()
            if not item:
                return None

            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)

            session.commit()
            session.refresh(item)
            return item
        finally:
            session.close()

    # -----------------------------------------------------------
    # DELETE
    # -----------------------------------------------------------
    def delete_url(self, url_id: int):
        session = self.db()
        try:
            item = session.query(URLList).filter(URLList.id == url_id).first()
            if not item:
                return False

            session.delete(item)
            session.commit()
            return True
        finally:
            session.close()
