from sqlalchemy import Boolean, Column, Integer, String, ARRAY

from db import Base

class Camp(Base):
    __tablename__ = "camps"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    tags = Column(ARRAY(String))
    image_urls = Column(ARRAY(String))