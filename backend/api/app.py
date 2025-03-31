from flask import Flask, request
import postgresqlite
from sqlalchemy.orm import registry
from models import db, Chore, Resident, Household
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import json
import functools
from dotenv import dotenv_values
import jwt
from datetime import datetime

# TODO:
# create house overview
# on the householdPage filtering should be done on the front end to reduce
# unnecessary request sending
# figure out a way if getting the chart to work is even a good idea and is worth it
# seperate the table out into components to stop useless template repetition

# create profile page


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlite.get_uri()
app.config['SECRET  _KEY'] = 'MEGA super duper secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.debug = True

# figure out a way to associate the chore with a user.
db.init_app(app)
mapper_registry = registry()
CORS(app)
mapper_registry.configure()

config = dotenv_values('.env')

CHORES_LIST = [
    ('Vacuum', False),
    ('Clean the Toilet', False),
    ('Mop the floor', False),
    ('Clean the Fridge', True),
    ('Kitchen sink', False),
    ('Take out the bins', False),
    ('Clean the stove', False),
    ('Wipe kitchen counter', False),
    ('Clean the shelf/sink in the shower', False),
    ('Shower Gutter', False),
    ('Wipe off the bar', False),
    ('Wipe off coffee tables,', False),
    ('Beat the carpets', True),
    ('Clear belongings out of communal areas', False),
]


def insert_chores(_list):
    for description, big_job in _list:
        db.session.add(Chore(description=description, is_big_job=big_job, household_id=4))

    db.session.commit()


def auth_jwt(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization').split(': ')[1]

        if not token:
            return {'error': 'No token or invalid token was provided.'}, 403
        
        decoded = jwt.decode(token, key=config['secretKey'], algorithms=['HS256'])
        
        if not decoded['user_id'] or not decoded['username']:
            return {'error': 'No token or invalid token was provided.'}, 403

        existing_user = db.session.query(Resident).filter(Resident.id == decoded['user_id']).first()
        
        if not existing_user:
            return {'error': 'No token or invalid token was provided.'}, 403

        return func(*args, user=existing_user, **kwargs)

    return wrapper


@app.route('/login', methods=["POST"])
def login():
    req_body = json.loads(request.data.decode())
    user = db.session.query(Resident).filter(Resident.name == req_body['username']).first()

    if not user:
        return {'error': 'User does not exist. Register instead.'}, 404

    if not bcrypt.check_password_hash(user.password, req_body['password']):
        return {'error': 'Username or password did not match'}, 403

    payload_data = {
        'username': req_body['username'],
        'user_id': user.id
    }

    token = jwt.encode(payload=payload_data, key=config['secretKey'])

    return {'status': 'ok', 'user': user.to_dict(), 'token': token}, 200


@app.route('/register', methods=['POST'])
def register():
    req_body = json.loads(request.data.decode())
    
    if not req_body['username'] or not req_body['password']:
        return {'error': 'Username and password required'}, 400

    existing_user = db.session.query(Resident).filter(Resident.name == req_body['username']).first()

    if existing_user:
        return {'error': 'User exists.'}, 403
    
    hashed_password = bcrypt.generate_password_hash(req_body['password']).decode('utf-8')

    db.session.add(Resident(name=req_body['username'], password=hashed_password))
    db.session.commit()
    
    new_user = db.session.query(Resident).filter(Resident.name == req_body['username']).first()
    
    return {'status': "ok", 'user': new_user.to_dict()}, 200


@app.route('/user/household', methods=['GET'])
@auth_jwt
def get_household(**kwargs):
    user = kwargs.get('user')
    if not user:
        return {'error': 'internal server error'}, 503
    
    if not user.household:
        return {'household': None}
    
    return {'household': user.household.to_dict()}
    

@app.route('/chore/<int:chore_id>', methods=['POST'])
@auth_jwt
def mark_chore_done(chore_id, **kwargs):
    chore = db.session.query(Chore).filter(Chore.id == chore_id).first()
    chore.is_done = True
    chore.done_on = datetime.today().strftime('%Y-%m-%d')
    db.session.commit()
    return {'status': 'ok', 'chore': chore.to_dict()}


@app.route('/household/<int:household_id>/chore/<status>', methods=["GET"])
@auth_jwt
def get_chores(household_id, status, **kwargs):
    """
    household_id: int
    status: string accepted: 'done' | 'todo' | 'all'
    """
    user = kwargs.get('user')

    if not user:
        return {'error': "internal server error"}, 503

    base_query = db.session.query(Chore).filter(
        Chore.resident_id == user.id,
        Chore.household_id == household_id,
    )

    if status == 'done':
        chores = base_query.filter(Chore.is_done == True).all()  # noqa: E712

    elif status == 'todo':
        chores = base_query.filter(Chore.is_done == False).all() # noqa: E712
    else:
        chores = base_query.all()

    return {'status': 'ok', 'chores': [chore.to_dict() for chore in chores]}


@app.route('/household/create', methods=["POST"])
@auth_jwt
def create_household(**kwargs):
    user = kwargs.get('user')

    if not user:
        return {'error': 'internal server error'}, 503

    req_body = json.loads(request.data.decode())

    if not req_body['name'] or not req_body['password']:
        return {'error': 'Name and password required'}, 403

    existing_household = db.session.query(Household).filter(Household.name == req_body['name']).first()

    if existing_household:
        return {'error': 'Household exists with that name. Repeat household names will be introduced later.'}, 403

    hashed_password = bcrypt.generate_password_hash(req_body['password']).decode('utf-8')

    household = Household(name=req_body['name'], password=hashed_password)
    db.session.add(household)
    db.session.commit()

    user.household_id = household.id

    db.session.commit()

    return {
        'status': 'ok',
        'household': household.to_dict(),
    }


@app.route('/user/household', methods=['POST'])
@auth_jwt
def associate_household(**kwargs):
    user = kwargs.get('user')

    if not user:
        return {'error': 'internal server error'}, 503

    req_body = json.loads(request.data.decode())

    household = db.session.query(Household).filter(Household.name == req_body['householdName']).first()

    if not bcrypt.check_password_hash(household.password, req_body['password']):
        return {'error': 'Household doesn\'t exist or incorrect password'}, 403

    user.household_id = household.id

    db.session.commit()

    return {'status': 'ok',
            'user': user.to_dict(),
            # myb ill need it idk
            # 'household': household.to_dict()
        }


with app.app_context():
    db.create_all()
    db.session.commit()

    chores = db.session.query(Chore).all()

    if not chores:
        insert_chores(CHORES_LIST)

if __name__ == "__main__":
    app.run(debug=True)
