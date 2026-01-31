from sqlalchemy import Column, Integer, String
from database import Base

# 1. Inherit from Base
class Log(Base):
    # 2. The Table Name
    __tablename__ = "logs"

    # 3. The Columns
    id = Column(Integer, primary_key=True, index=True)
    
    # We want to save "14:30"
    input_time = Column(String)
    
    # We want to save "IST (Indian Standard Time)"
    location = Column(String)
    
    # We want to save "+5:30"
    calculated_offset = Column(String)

    # We want to save the IP address of the user
    ip_address = Column(String)