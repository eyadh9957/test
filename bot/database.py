from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class User(Base):
    """Discord user model."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    discord_token = Column(LargeBinary, nullable=True)  # Encrypted token
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sessions = relationship('Session', back_populates='user', cascade='all, delete-orphan')

class Session(Base):
    """Quest completion sessions."""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    quests_completed = Column(Integer, default=0)
    status = Column(String, default='active')  # active, paused, completed, stopped
    
    # Relationships
    user = relationship('User', back_populates='sessions')

class QuestLog(Base):
    """Log of completed quests."""
    __tablename__ = 'quest_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quest_name = Column(String, nullable=False)
    reward = Column(Integer, default=0)  # XP/rewards earned
    completed_at = Column(DateTime, default=datetime.utcnow)

class Database:
    """Database handler."""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        logger.info('Database initialized')
    
    def get_session(self):
        """Get a new database session."""
        return self.SessionLocal()
    
    def create_user(self, discord_id: str, username: str, token: bytes = None):
        """Create a new user."""
        session = self.get_session()
        try:
            user = User(discord_id=discord_id, username=username, discord_token=token)
            session.add(user)
            session.commit()
            logger.info(f'Created user: {discord_id}')
            return user
        except Exception as e:
            session.rollback()
            logger.error(f'Error creating user: {e}')
            raise
        finally:
            session.close()
    
    def get_user(self, discord_id: str):
        """Get user by Discord ID."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.discord_id == discord_id).first()
        finally:
            session.close()
    
    def link_token(self, discord_id: str, encrypted_token: bytes):
        """Link a Discord token to a user."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.discord_id == discord_id).first()
            if user:
                user.discord_token = encrypted_token
                session.commit()
                logger.info(f'Token linked for user {discord_id}')
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f'Error linking token: {e}')
            raise
        finally:
            session.close()
    
    def log_quest_completion(self, discord_id: str, quest_name: str, reward: int = 0):
        """Log a completed quest."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.discord_id == discord_id).first()
            if user:
                log = QuestLog(user_id=user.id, quest_name=quest_name, reward=reward)
                session.add(log)
                session.commit()
                logger.info(f'Logged quest completion: {quest_name} for {discord_id}')
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f'Error logging quest: {e}')
            raise
        finally:
            session.close()
