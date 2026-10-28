from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class TodoTask(Base):

    __tablename__ = "todo_tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    completed = Column(
        Boolean,
        default=False
    )

    user = relationship(
        "User",
        backref="todos"
    )