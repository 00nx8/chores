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

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlite.get_uri()
app.config['SECRET_KEY'] = 'MEGA super duper secret key'
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


def auth_jtw(func):
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
@auth_jtw
def get_household(**kwargs):
    user = kwargs.get('user')
    if not user:
        return {'error': 'internal server error'}, 503
    
    if not user.household:
        return {'household': None}
    
    return {'household': user.household.to_dict()}
    

@app.route('/household/create', methods=["POST"])
@auth_jtw
def create_household(**kwargs):
    user = kwargs.get('user')

    if not user:
        return {'error': 'internal server error'}, 503

    req_body = json.loads(request.data.decode())

    if not req_body['name'] or not req_body['password']:
        return {'error': 'Name and password required'}

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
@auth_jtw
def associate_household(**kwargs):
    user = kwargs.get('user')

    if not user:
        return {'error': 'internal server error'}, 503

    req_body = json.loads(request.data.decode())

    # compare household password with submitted password
    # if all checks out mark resident.household_id = household.id

    return {'stats': 'valid endpoint g'}


def insert_chores(_list):
    for description, big_job in _list:
        db.session.add(Chore(description=description, is_big_job=big_job))

    db.session.commit()


with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
