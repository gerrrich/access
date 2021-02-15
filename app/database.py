from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

from flask_login import UserMixin

from app import db

Lesson_Students = Table('Lesson_Students', db.metadata,
                        Column('lesson', Integer, ForeignKey('Lesson.id')),
                        Column('student', Integer, ForeignKey('Student.id')))
Student_Subjects = Table('Student_Subjects', db.metadata,
                         Column('student', Integer, ForeignKey('Student.id')),
                         Column('subject', Integer, ForeignKey('Subject.id')))
Teacher_Subjects = Table('Teacher_Subjects', db.metadata,
                         Column('teacher', Integer, ForeignKey('Teacher.id')),
                         Column('subject', Integer, ForeignKey('Subject.id')))


class Admin(db.Model, UserMixin):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def create(self, admin):
        self.__user = admin
        return self

    def get_id(self):
        return self.__user.id

    def __repr__(self):
        return f"<account {self.id}>"


class Teacher(db.Model, UserMixin):
    __tablename__ = 'Teacher'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lessons = relationship('Lesson')
    subjects = relationship('Subject', secondary=Teacher_Subjects)

    def create(self, teacher):
        self.__user = teacher
        return self

    def get_id(self):
        return self.__user.id

    def __repr__(self):
        return f"<account {self.id}>"


class Student(db.Model, UserMixin):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    subjects = relationship('Subject', secondary=Student_Subjects)

    def create(self, student):
        self.__user = student
        return self

    def get_id(self):
        return self.__user.id

    def __repr__(self):
        return f"<account {self.id}>"


class Subject(db.Model):
    __tablename__ = 'Subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lessons = relationship('Lesson')


class Lesson(db.Model):
    __tablename__ = 'Lesson'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Boolean, nullable=False)
    format = db.Column(db.Boolean, nullable=False)
    topic = db.Column(db.String(100), nullable=True)
    late_time = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Integer, ForeignKey('Subject.id'), nullable=False)
    teacher = db.Column(db.Integer, ForeignKey('Teacher.id'), nullable=False)
    students = relationship('Student', secondary=Lesson_Students)
