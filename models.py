import os
import psycopg2
from flask import Flask
from sqlalchemy import (Column, String, Integer, Table, ForeignKey)
from flask_sqlalchemy import SQLAlchemy
import json



database_name = "castdb"
database_path = 'postgres://jpqtvpjtrzhsir:4f24f0ca7d0131ba3ba5d4908469b8b5b2b5496b237f5867a169362365824c09@ec2-35-171-57-132.compute-1.amazonaws.com:5432/dhd0uim8bmdo'
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
   

# def init_db():
#     db.drop_all()
#     db.create_all()

'''
Movies
Have title and release Date
'''
class Movies(db.Model):  
  __tablename__ = 'movies'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String(250))
  release_date = Column(db.String(250))

  def __init__(self, name, release_date):
    self.name = name
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'release_date': self.release_date}

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
        db.session.delete(self)
        db.session.commit()

  def update(self):
        db.session.commit()


'''
Actors
Have name, age and gender
'''
class Actors(db.Model):  
  __tablename__ = 'actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String(250))
  age = Column(db.Integer)
  gender = Column(db.String(250))

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}
  

  def __repr__(self):
        return json.dumps(self.format())

  
  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
        db.session.delete(self)
        db.session.commit()

  def update(self):
        db.session.commit()

  