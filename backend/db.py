from sqlalchemy import Column, Float, Integer, String, Text, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./palmystery.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    birth_date = Column(String, nullable=True)
    birth_time = Column(String, nullable=True)
    birth_place = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


class DailyRashifal(Base):
    __tablename__ = "daily_rashifal"
    __table_args__ = (UniqueConstraint("date_ad", "rashi", name="uq_date_rashi"),)

    id = Column(Integer, primary_key=True, index=True)
    date_ad = Column(String, index=True, nullable=False)
    rashi = Column(String, nullable=False)
    text_ne = Column(Text, nullable=False)
    text_en = Column(Text, nullable=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
