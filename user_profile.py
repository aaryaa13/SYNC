from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class UserProfile(Base):

    __tablename__ = "user_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    height = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Integer,
        nullable=False
    )

    last_period = Column(
        Date,
        nullable=False
    )

    cycle_length = Column(
        Integer,
        nullable=False
    )

    period_duration = Column(
        Integer,
        nullable=False
    )

    next_period = Column(
        String(50),
        nullable=True
    )

    current_phase = Column(
        String(50),
        nullable=True
    )

    user = relationship(
        "User",
        backref="profile"
    )