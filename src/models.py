from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planet = db.relationship('Favorite_Planet', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_planet": list(map(lambda x: x.serialize(), self.favorite_planet))

            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    population = db.Column(db.Float, nullable=False)
    galaxy = db.Column(db.String(80), nullable=False)
    empire_ally = db.Column(db.Boolean(), nullable=False)


    def __repr__(self):
        return '<Planetas %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "galaxy": self.galaxy,
            "empire_ally": self.empire_ally,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    race = db.Column(db.String(80), nullable=False)
    language = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "language": self.language,
            "age": self.age,
            # do not serialize the password, its a security breach
        }


class Favorite_Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("User.id"))
    character_id = db.Column(db.Integer, ForeignKey('Characters.id'))

    def __repr__(self):
        return '<Favorite_Character %r>' % self.character_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }


class Favorite_Planet(db.Model):
    # Here we define Columns for the table address.
    # Notice that each Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, ForeignKey('Planets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    def __repr__(self):
        return '<Favorite_Planet %r>' % self.planet_id

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }
