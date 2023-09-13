from sqlalchemy import Column, Integer, String, ARRAY

from db import Base

class Camp(Base):
    __tablename__ = "camps"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phoneNumber = Column(String)
    description = Column(String)
    campType = Column(String)
    tags = Column(ARRAY(String), default=[])
    image_urls = Column(ARRAY(String), default=[])
    website = Column(String)
    streetAddress = Column(String)
    city = Column(String)
    state = Column(String)
    zipCode = Column(String)
    country = Column(String)
    aptSuiteOther = Column(String)