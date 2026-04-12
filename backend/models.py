from sqlalchemy import Column, Integer, String
from database import Base

# 🔐 USER TABLE (for login/signup)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)


# 💬 CHAT TABLE (for chat history)
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    message = Column(String)
    reply = Column(String)