import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from utils.settings import settings

engine = sa.create_engine(settings.DB_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    is_processed = sa.Column(sa.Boolean, nullable=False, default=False)
    process_datetime = sa.Column(sa.DateTime, nullable=True)


class Title(Base):
    __tablename__ = "titles"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64), nullable=False)
    timestamp = sa.Column(sa.DateTime, nullable=True)
    name_rus = sa.Column(sa.String(64), nullable=False)
    rate = sa.Column(sa.Integer(), nullable=False)
    episodes = sa.Column(sa.Integer(), nullable=True)
    kind = sa.Column(sa.String(20), nullable=False)
    status = sa.Column(sa.String(20), nullable=False)


class UserRate(Base):
    __tablename__ = "user_rates"
    __table_args__ = (sa.PrimaryKeyConstraint("user_id", "title_id"),)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    title_id = sa.Column(sa.Integer)
    rate = sa.Column(sa.Integer, nullable=False)
