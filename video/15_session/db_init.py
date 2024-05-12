import datetime

from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing_extensions import Annotated
from typing import List


class Base(DeclarativeBase):
    pass


class Base2(DeclarativeBase):
    pass


engine = create_engine('mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8', echo=True)
engine2 = create_engine('mysql://root:test@localhost/myblog_db', echo=True)


int_pk = Annotated[int, mapped_column(primary_key=True)]
required_unique_string = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]
required_string = Annotated[str, mapped_column(String(128), nullable=False)]
timestamp_not_null = Annotated[datetime.datetime, mapped_column(nullable=False)]


class User(Base2):
    __tablename__ = "users"

    id: Mapped[int_pk]
    name: Mapped[required_unique_string]

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class Department(Base):
    __tablename__ = "department"

    id: Mapped[int_pk]
    name: Mapped[required_unique_string]

    employees: Mapped[List["Employee"]] = relationship(back_populates="department")

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int_pk]
    dep_id: Mapped[int] = mapped_column(ForeignKey("department.id"))
    name: Mapped[required_unique_string]
    birthday: Mapped[timestamp_not_null]

    department: Mapped[Department] = relationship(back_populates="employees")

    def __repr__(self):
        return f'id: {self.id}, dep_id: {self.dep_id}, name: {self.name}, birthday: {self.birthday}'


Base.metadata.create_all(engine)
Base2.metadata.create_all(engine2)
