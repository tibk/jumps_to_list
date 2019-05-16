import os
import sys
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Jumper(Base):
    __tablename__ = 'jumper'
    # Here we define columns for the table jumper
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Spot(Base):
    __tablename__ = 'spot'
    # Here we define columns for the table spot
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    location = Column(String(250), nullable=False)
    height = Column(Integer, nullable=False)


class Suit(Base):
    __tablename__ = 'suit'
    # Here we define columns for the table suit
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    brand = Column(String(250), nullable=False)
    kind = Column(String(250), nullable=False)


class JumpKind(Base):
    __tablename__ = 'jump_kind'
    # Here we define columns for the table jump_kind
    id = Column(Integer, primary_key=True)
    kind = Column(String(250), nullable=False)


class Jump(Base):
    __tablename__ = 'jump'
    # Here we define columns for the table jump
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    jumper_id = Column(Integer, ForeignKey('jumper.id'))
    spot_id = Column(Integer, ForeignKey('spot.id'))
    suit_id = Column(Integer, ForeignKey('suit.id'))
    jump_kind_id = Column(Integer, ForeignKey('jump_kind.id'))
    number = Column(Integer, nullable=False)
    comments = Column(String(500))
    UniqueConstraint(jumper_id, number, name='jump_number_unique_per_jumper')

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('postgresql://tkarrer@localhost/base_statistics')


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
