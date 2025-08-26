from datetime import datetime
import json
import functools
from models import db, Chore, Resident, Household, ChoreCompletion
from flask import Flask, request
from sqlalchemy.orm import registry
from sqlalchemy import literal_column, func
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import dotenv_values
import jwt
from datetime import datetime, timedelta
# TODO:
# figure out deadline tracking for each chore.
    # How to keep track of on time 
    # make a table that stores chore_id, resident_id, deadline, chore.done_on
    # can be referenced/updated when needed. 
    # deadline can serve as a period to query by.


# create house overview
    # add an option to view residents, with delete option

# create profile page
    # overview of all the todos for this person

# turn into mobile app
    # cron jobs for scheduling and assigning chores
    # notifications

app = Flask(__name__)
bcrypt = Bcrypt(app)
config = dotenv_values('.env')

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URL']
app.config['SECRET_KEY'] = 'MEGA super duper secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.debug = True

# figure out a way to associate the chore with a user.
db.init_app(app)
mapper_registry = registry()
CORS(app)
mapper_registry.configure()


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
    user = kwargs.get('user')
    resident = db.session.query(Resident).filter(user.id == Resident.id).first()
    chore = db.session.query(Chore).filter(Chore.id == chore_id).first()

    completion = ChoreCompletion(
            chore_id=chore_id,
            resident_id=resident.id,
            household_id=resident.household_id
        )

    completion.done_on = datetime.today()
    completion.deadline = chore.deadline

    db.session.add(completion)
    db.session.commit()
    return {'status': 'ok', 'chore': chore.to_dict(), 'completion': completion.to_dict()}



@app.route('/household/<int:household_id>/chore', methods=["GET"])
@auth_jwt
def get_chores(household_id, **kwargs):
    """
    household_id: int
    """
    user = kwargs.get('user')
    if not user:
        return {'error': "internal server error"}, 503

    chores = db.session.query(Chore).filter(Chore.household_id == household_id).all()

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

    chore = Chore(name=name, description=description, household_id=household_id)

    chore.repeat_schedule = int(req_body.get('frequency'))

    chore.deadline = datetime.today() + timedelta(days=chore.repeat_schedule)

    if doing_it:
        chore.resident_id = doing_it

    db.session.add(chore)
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
            'user': user.to_dict()
        }


@app.route('/user', methods=["GET"])
@auth_jwt
def get_current_user(**kwargs):
    user = kwargs.get('user')
    if not user:
        return {'error': 'Token passed authentication but no user was found.'}
    household = user.household
    chores = db.session.query(Chore).filter(Chore.resident_id == user.id).all()
    
    return {'status':'ok', "user": user.to_dict(), "chores": [chore.to_dict() for chore in chores], "household": household.to_dict() if household else {}}

@app.route('/chore', methods=["DELETE"])
@auth_jwt
def delete_chore(**kwargs):
    req_body = json.loads(request.data.decode())
    
    delete_count = db.session.query(Chore).filter(Chore.id == req_body['choreId']).delete()

    db.session.commit()

    if not delete_count:
        return {'status': 'error', 'error': 'Chore with given ID does not exist.'}, 404
    
    return {'status': 'ok'}

@app.route('/household/<int:household_id>/done', methods=['GET'])
@auth_jwt
def get_done_chores(household_id, **kwargs):
    recent_done_chores = db.session.query(ChoreCompletion) \
        .join(Chore, Chore.id == ChoreCompletion.chore_id) \
        .filter(ChoreCompletion.household_id == household_id).all()
        # .filter(
        #         ChoreCompletion.done_on > func.now() - (literal_column("interval '1 day'") * Chore.repeat_schedule))
    
    return {'status': 'ok', 'chores': [chore.to_dict() for chore in recent_done_chores]}


def populate_schema():
    import random
    from datetime import datetime, timedelta

    # === 1. Generate Random Chores ===

    sample_chore_names = [
        "Take out trash", "Clean kitchen", "Vacuum living room",
        "Water plants", "Feed the cat", "Laundry", "Grocery shopping"
    ]

    chores = []
    for i in range(5):
        name = random.choice(sample_chore_names)
        description = f"{name} - auto generated"
        repeat_schedule = random.choice([1, 3, 7, 14])
        deadline = datetime.now() + timedelta(days=random.randint(1, 7))

        chore = Chore(
            name=name,
            description=description,
            repeat_schedule=repeat_schedule,
            deadline=deadline,
            resident_id=1,
            household_id=1
        )
        chores.append(chore)
    db.session.add_all(chores)
    db.session.commit()

    # === 2. Generate Random Chore Completions ===

    chore_completions = []
    for i in range(5):
        chore = random.choice(chores)
        days_ago_done = random.randint(0, 90)
        done_on = datetime.now() - timedelta(days=days_ago_done)
        # Deadline is before done_on (by 1 to 7 days)
        deadline = done_on - timedelta(days=random.randint(1, 7))

        completion = ChoreCompletion(
            chore_id=chore.id,
            resident_id=1,
            household_id=1,
            done_on=done_on,
            deadline=deadline
        )
        chore_completions.append(completion)
        db.session.add_all(chore_completions)
        db.session.commit()


with app.app_context():
    db.create_all()
    # populate_schema()
    db.session.commit()

if __name__ == "__main__":
    app.run()
