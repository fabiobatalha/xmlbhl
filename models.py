from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database/xmlbhl.db', echo=True)
Session = sessionmaker()
Base = declarative_base()


class Upload(Base):
    __tablename__ = 'upload'

    id = Column(Integer, primary_key=True)
    filename = Column(String(128), unique=True)
    uploaded_at = Column(String(16))
    source = Column(String())

    def __init__(self, filename, uploaded_at, source):
        self.filename = filename
        self.uploaded_at = uploaded_at
        self.source = source

    def __repr__(self):
        return "<Upload('%s')>" % (self.filename)
