from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    
    attr_hashing = None
    attr_encrypted = None