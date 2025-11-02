"""
POC 12: Database Models for Authentication
SQLAlchemy ORM models for users and authentication
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    """User account model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))  # NULL for OAuth-only users
    full_name = Column(String(255))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    oauth_connections = relationship("OAuthConnection", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"


class OAuthConnection(Base):
    """OAuth provider connections"""
    __tablename__ = 'oauth_connections'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    provider = Column(String(50), nullable=False, index=True)  # 'google', 'facebook', 'microsoft'
    provider_user_id = Column(String(255), nullable=False)
    provider_email = Column(String(255))
    provider_name = Column(String(255))
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="oauth_connections")
    
    def __repr__(self):
        return f"<OAuthConnection(id={self.id}, provider='{self.provider}', user_id={self.user_id})>"


class RefreshToken(Base):
    """Refresh tokens for JWT authentication"""
    __tablename__ = 'refresh_tokens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False, index=True)
    revoked_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"


class PasswordResetToken(Base):
    """Password reset tokens"""
    __tablename__ = 'password_reset_tokens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False, index=True)
    used_at = Column(DateTime)
    
    def __repr__(self):
        return f"<PasswordResetToken(id={self.id}, user_id={self.user_id}, used={self.used})>"


def get_db_engine(database_url: str):
    """Create database engine"""
    return create_engine(database_url, echo=False)


def get_session_maker(engine):
    """Create session maker"""
    return sessionmaker(bind=engine)


def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(engine)


def drop_tables(engine):
    """Drop all tables from the database"""
    Base.metadata.drop_all(engine)
