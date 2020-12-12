from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

from flask_login import UserMixin

from app import db

Subjects_Users = Table('Subjects_Users', db.metadata,
    Column('subject_id', Integer, ForeignKey('Subject.id')),
    Column('user_id', Integer, ForeignKey('User.id'))
)


Works_Students = Table('Works_Students', db.metadata,
    Column('work_id', Integer, ForeignKey('Work.id')),
    Column('student_id', Integer, ForeignKey('User.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    accountLogin = db.Column(db.String(100), nullable=False, unique=False)
    accountPassword = db.Column(db.String(500), nullable=False)
    fullName = db.Column(db.String(100), nullable=False)
    accountType = db.Column(db.Integer, nullable=False)
    subjects = relationship("Subject", secondary=Subjects_Users, back_populates="users")


    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return self.__user.id

    def __repr__(self):
        return f"<account {self.id}>"


class Work(db.Model):
    __tablename__ = 'Work'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(500), nullable=False)
    subject = db.Column(Integer, ForeignKey('Subject.id'), nullable=False)
    type_work = db.Column(db.Boolean, nullable=False)
    how_work = db.Column(db.Boolean, nullable=False)
    topic = db.Column(db.String(500))
    late_time = db.Column(db.Integer, nullable=False)
    teacher =
    students = relationship("User", secondary=Works_Students)


class Subject(db.Model):
    __tablename__ = 'Subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    users = relationship("User", secondary=Subjects_Users, back_populates="subjects")
    works = relationship("Work")