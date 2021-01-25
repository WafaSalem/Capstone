from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from flask_sqlalchemy import SQLAlchemy
import os
import json
from sqlalchemy.orm import relationship

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Authors(db.Model):  
  __tablename__ = 'authors'

  id = Column(Integer, primary_key=True)
  auth_name = Column(String)
  auth_gender = Column(String)
  relate=relationship('Books',backref='auth_book',lazy=True)
  

  def __init__(self, auth_name, auth_gender):
    self.auth_name=auth_name
    self.auth_gender=auth_gender
  
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'auth_name': self.auth_name,
      'auth_gender': self.auth_gender}
   

class Books(db.Model):  
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True)
  book_name = Column(String)
  book_type = Column(String)
  book_rate =Column(Integer)
  auth_id=Column(Integer,ForeignKey("authors.id"))

  def __init__(self, book_name, book_type ,book_rate ):
    self.book_name= book_name
    self.book_type = book_type
    self.book_rate= book_rate

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'book_name': self.book_name,
      'book_type': self.book_type,
      'book_rate': self.book_rate,
      'auth_id':self.auth_book.id
      }
  


