from datetime import datetime
import json
import functools
from models import db, Chore, Resident, Household, ResidentChores, HouseholdChore
from flask import Flask, request
import postgresqlite
from sqlalchemy.orm import registry
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import dotenv_values
import jwt

# TODO:
# create house overview
    # add an option to view residents, with delete option
# create profile page
    # overview of all the todos for this person
# some kind of nav option
# turn into mobile app
    # cron jobs for scheduling and assigning chores
    # notifications

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
    ('Vacuum', 'False'),
    ('Clean the Toilet', 'False'),
    ('Mop the floor', 'False'),
    ('Clean the Fridge', 'True'),
    ('Kitchen sink', 'False'),
    ('Take out the bins', 'False'),
    ('Clean the stove', 'False'),
    ('Wipe kitchen counter', 'False'),
    ('Clean the shelf/sink in the shower', 'False'),
    ('Shower Gutter', 'False'),
    ('Wipe off the bar', 'False'),
    ('Wipe off coffee tables,', 'False'),
    ('Beat the carpets', 'True'),
    ('Clear belongings out of communal areas', 'False'),
]

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
    """ 
    Endpoint for logging in.
    method: post
    Requires body/password to be attached to the request body. 
    """
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


@app.route('/household/<int:household_id>/residents', methods=['GET'])
@auth_jwt
def get_users(household_id, **kwargs):
    residents = db.session.query(Resident).filter(Resident.household_id == household_id).all()
    return {'status': 'ok', "residents": [resident.to_dict() for resident in residents]}

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


@app.route('/household/<int:household_id>/chore', methods=["GET"])
@auth_jwt
def get_chores(household_id, **kwargs):
    """
    household_id: int
    """
    user = kwargs.get('user')
    if not user:
        return {'error': "internal server error"}, 503

    chores = db.session.query(Chore).join(HouseholdChore, Chore.id == HouseholdChore.chore_id) \
        .filter(household_id == HouseholdChore.household_id).all()

    return {'status': 'ok', 'chores': [chore.to_dict() for chore in chores]}


@app.route('/household', methods=["POST"])
@auth_jwt
def create_household(**kwargs):
    """requires logged in user,
    requires name and password in request body

    """
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

@app.route('/chore', methods=["POST"])
@auth_jwt
def add_chore(**kwargs):
    req_body = json.loads(request.data.decode())

    if not req_body.get('name'):
        return {'error': 'No name was provided'}, 403
    
    name = req_body.get('name')
    description = req_body.get('description')
    doing_it = req_body.get('doing_it')

    household_id = req_body.get('household_id')

    chore = Chore(name=name, description=description)

    if doing_it:
        chore.doing_it = doing_it

    db.session.add(chore)
    db.session.commit()

    if household_id:
        household_chore = HouseholdChore(chore_id=chore.id, household_id=household_id)
        db.session.add(household_chore)
        db.session.commit()

    return {"status": "ok", "chore": chore.to_dict()}


@app.route('/user/household', methods=['POST'])
@auth_jwt
def associate_household(**kwargs):
    user = kwargs.get('user')

    if not user:
        return {'error': 'internal server error'}, 503

    req_body = json.loads(request.data.decode())

    household = db.session.query(Household).filter(Household.name == req_body['name']).first()

    if not household:
        return {'error': 'requested household not found'}, 404

    if not bcrypt.check_password_hash(household.password, req_body.get('password')):
        return {'error': 'Household doesn\'t exist or incorrect password'}, 403

    user.household_id = household.id
    db.session.commit()

    return {'status': 'ok',
            'user': user.to_dict(),
            # myb ill need it idk
            # 'household': household.to_dict()
        }
@app.route('/user/profile_picture', methods=["POST"])
@auth_jwt
def set_profile_picture(**kwargs):
    user = kwargs.get('user')
    req_body = json.loads(request.data.decode())

    if not req_body.get('profile_picture'):
        return {'error': 'Please attach a profile picture'}, 400

    return {'status': 'ok'}


@app.route('/user', methods=["GET"])
@auth_jwt
def get_current_user(**kwargs):
    user = kwargs.get('user')
    print(user)
    if not user:
        return {'error': 'Token passed authentication but no user was found.'}
    
    household = user.household
    chores = db.session.query(Chore).filter(Chore.doing_it == user.id).all()
    
    return {'status':'ok', "user": user.to_dict(), "chores": [chore.to_dict() for chore in chores], "household": household.to_dict()}

with app.app_context():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
