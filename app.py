from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from config import TestingConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)

# ================== DATABASE ==================

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


# CLI: flask <command>

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name="Mercury",
                     planet_type="Class D",
                     home_star="Sol",
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)
    venus = Planet(planet_name="Venus",
                   planet_type="Class K",
                   home_star="Sol",
                   mass=4.258e23,
                   radius=3760,
                   distance=77.24e6)
    earth = Planet(planet_name="Earth",
                   planet_type="Class M",
                   home_star="Sol",
                   mass=5.972e24,
                   radius=3959,
                   distance=92.96e6)
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name="William",
                     last_name="Herschel",
                     email="william_hershel@gmail.com",
                     password="password")
    db.session.add(test_user)

    db.session.commit()
    print('Database seeded!')


# ================== ROUTES ==================


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from Planetary API!!'), 200


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message=f"Sorry, {name}, you are not old enough."), 401
    else:
        return jsonify(message=f"Welcome, {name}, you are old enough!")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message=f"Sorry, {name}, you are not old enough."), 401
    else:
        return jsonify(message=f"Welcome, {name}, you are old enough!")



if __name__ == '__main__':
    app.run()
