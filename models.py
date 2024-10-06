from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



class Post(Base): # sqlalchemy base model
    __tablename__ = "Another_new_posts"


    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default='TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("USERS_INFO.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")
#   cannot modify these things after the creation like changing nullabe to True, otherwise delete the table & run this again
#   To change use Alembic

########################################################################################################################################


class User(Base):
    __tablename__ = "USERS_INFO"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False) 
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))



########################################################################################################################################

class Vote(Base):
    __tablename__ = "votess"
    user_id = Column(Integer, ForeignKey("USERS_INFO.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("Another_new_posts.id", ondelete="CASCADE"), primary_key=True)