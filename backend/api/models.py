from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship

db = SQLAlchemy()
# new database
# update app.py to refer to these models
class Household(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)

    user = relationship('User', back_populates='household')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Resident(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)

    household_id = sa.Column(sa.Integer, sa.ForeignKey('household.id'), nullable=True)
    household = relationship('Household', back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'household_id': self.household_id
        }

    
class Chore(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    is_done = sa.Column(sa.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class ResidentChores(db.Model):
    resident_id = sa.Column(sa.ForeignKey('resident.id'), primary_key=True)
    chore_id = sa.Column(sa.ForeignKey('chore.id'), primary_key=True)
    
class HouseholdChore(db.Model):
    household_id = sa.Column(sa.ForeignKey('household.id'), primary_key=True)
    chore_id = sa.Column(sa.ForeignKey('chore.id'), primary_key=True)
    
# class Household(db.Model):
#     """
#     name: string
#     password: string
#     """
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String, nullable=False)
#     password = sa.Column(sa.String, nullable=False)

#     # ## Relationships
#     # Resident
#     resident = relationship('Resident', back_populates='household')
#     # Chore
#     chore = relationship('Chore', back_populates='household')

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#         }


# class Resident(db.Model):
#     """
#     name: string
#     password: string
#     household_id: int
#     """
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String, nullable=False)
#     password = sa.Column(sa.String, nullable=False)
    
#     # ## Relationships
    
#     # chores
#     chore_to_do = relationship('Chore', back_populates='doer')

#     # Household
#     household = relationship('Household', back_populates='resident')
#     household_id = sa.Column(sa.Integer, sa.ForeignKey('household.id'), nullable=True)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'household_id': self.household_id
#         }
    

# class Chore(db.Model):
#     """
#     description: string
#     deadline: datetime
#     done_on: datetime, nullable
#     is_big_job: boolean, default=false
#     is_done: boolean default=false
#     """
#     id = sa.Column(sa.Integer, primary_key=True)
#     description = sa.Column(sa.String, nullable=False)
#     deadline = sa.Column(sa.DateTime, nullable=True)
#     done_on = sa.Column(sa.DateTime, nullable=True)
#     is_big_job = sa.Column(sa.Boolean, default=False, nullable=False)
#     is_done = sa.Column(sa.Boolean, default=False, nullable=False)

#     # ## Relationships
#     # Resident
#     doer = relationship('Resident', back_populates="chore_to_do")
#     resident_id = sa.Column(sa.Integer, sa.ForeignKey('resident.id'), nullable=True)

#     # Household
#     household = relationship('Household', back_populates='chore')
#     household_id = sa.Column(sa.Integer, sa.ForeignKey('household.id'), nullable=False)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'desc': self.description,
#             'deadline': self.deadline,
#             'done_on': self.done_on,
#             'resident_id': self.resident_id,
#             'is_done': self.is_done
#         }
