from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Household(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)

    user = relationship('Resident', back_populates='household')

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
    is_done = sa.Column(sa.Boolean, nullable=False, default=False)
    repeat_schedule = sa.Column(sa.Integer, nullable=False, default=7)

    doing_it = sa.Column(sa.Integer, sa.ForeignKey('resident.id'), nullable=True)
    resident = relationship(Resident, back_populates="doing_chore")

    def set_deadline(self):
        # once its been done for 3 days
        # it will be re assigned.

        pass

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_done': self.is_done,
            "doing_it": self.resident.name,
            "done_on": self.done_on,
            "deadline": self.deadline
        }

class ChoreCompletionTracker(db.Model):
    id = sa.Column(sa.Integer, sa.PrimaryKey)
    chore_id = sa.Column(sa.Integer, sa.ForeignKey('chore.id'), nullable=False)
    done_on = sa.Column(sa.DateTime, nullable=False)
    deadline = sa.Column(sa.DateTime, nullable=False)

# TODO:
# delete this garbage
class ResidentChores(db.Model):
    resident_id = sa.Column(sa.ForeignKey('resident.id'), primary_key=True)
    chore_id = sa.Column(sa.ForeignKey('chore.id'), primary_key=True)
# and this one
class HouseholdChore(db.Model):
    household_id = sa.Column(sa.ForeignKey('household.id'), primary_key=True)
    chore_id = sa.Column(sa.ForeignKey('chore.id'), primary_key=True)

