from app.backend.db import Base
from sqlalchemy import Column, Integer, String

class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    slug = Column(String, unique=True, index=True)



from sqlalchemy.schema import CreateTable
print(CreateTable(Tasks.__table__))

