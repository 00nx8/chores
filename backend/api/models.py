from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Household(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)

    user = relationship('Resident', back_populates='household')

    household_chore = relationship("Chore", back_populates="household")


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Resident(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    
    chores_done = sa.Column(sa.Integer, nullable=False, default=0)

    household_id = sa.Column(sa.Integer, sa.ForeignKey('household.id'), nullable=True)
    household = relationship('Household', back_populates='user')

    doing_chore = relationship('Chore', back_populates="resident")

    completed_chore = relationship('ChoreCompletion', back_populates='resident')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'household_id': self.household_id,
        }


class Chore(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    repeat_schedule = sa.Column(sa.Integer, nullable=False, default=7)

    deadline = sa.Column(sa.DateTime, nullable=True)

    resident_id = sa.Column(sa.Integer, sa.ForeignKey('resident.id'), nullable=True)
    resident = relationship(Resident, back_populates="doing_chore")

    household_id = sa.Column(sa.Integer, sa.ForeignKey('household.id'), nullable=False)
    household = relationship(Household, back_populates="household_chore")

    completion = relationship('ChoreCompletion', back_populates='chore')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'repeat_schedule': self.repeat_schedule,
            'deadline': self.deadline,
            'resident_id': self.resident_id,
            'household_id': self.household_id 
        }

class ChoreCompletion(db.Model):
    chore_id = sa.Column(sa.Integer, sa.ForeignKey('chore.id'),primary_key=True, nullable=False)
    resident_id = sa.Column(sa.Integer, sa.ForeignKey('resident.id'),primary_key=True, nullable=False)

    household_id = sa.Column(sa.Integer, nullable=False)
    done_on = sa.Column(sa.DateTime, nullable=False)
    deadline = sa.Column(sa.DateTime, nullable=False)

    chore = relationship('Chore', back_populates='completion')
    resident = relationship('Resident', back_populates='')

    def to_dict(self):
        return {
            'chore_id': self.chore_id,
            'resident_id': self.resident_id,
            'household_id': self.household_id,
            'done_on': self.done_on,
            'deadline': self.deadline
        }

