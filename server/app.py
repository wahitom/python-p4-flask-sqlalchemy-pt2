#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Owner, Pet

app = Flask(__name__)
# app.config points to our existign database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#  this is set to false to avoid building up too much unhelpful data in memory
#  when our app is running 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  this migrate instance configurs the app and models for flask migrate 
migrate = Migrate(app, db)

#  this connects our database to our app before it runs
db.init_app(app)

#  adding route to allow this info to be accessible through the internet 
#  @app.route determines which resources are available at which urls and saves 
#  the to the app's url map
@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        #  responses are what we return to the client after a request and this 
        #  included response ie 200 means the resource exists and is accessible 
        #  at the provided url
        200
    )
    return response 

#  create pet view 
@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    #  error handling 
    if not pet:
        response_body = '<h1>404 pet not found</h1>'
        response = make_response(response_body, 404)
        return response 

    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    response = make_response(response_body, 200)

    return response 

#  create owner view 
@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    # handle error if there are no such owners 
    if not owner:
        response_body = '<h1>404 owner not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'<h1>Information for {owner.name}</h1>'

    pets = [pet for pet in owner.pets]

    #  if owner exists but has no pets
    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    response = make_response(response_body, 200)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)


#  in the python shell you can add info to your database like this 
# >> from app import app
# >> from models import db, Owner, Pet

# >> pet = Pet(name="Ben", species="Dog")
# >> db.session.add(pet)
# >> db.session.commit()
# >> pet.id
#  => 1

# >> owner = Owner(name="Ben")
# >> db.session.add(owner)
# >> db.session.commit()
# >> owner
#  => <Pet Owner Ben>

# >> pet.owner = owner
# >> db.session.add(pet)
# >> db.session.commit()
# >> pet.owner
#  => <Pet Owner Ben> 
    

# Querying Flask sqlalchemy 

# deletions are best handled through the modles themselves and to retrieve all 
#  pets from the flask shell tyou woud run
    
# from models import db, Pet, Owner
# from app import app
# with app.app_context():
#    Pet.query.all()

#  => [<Pet Ben, Dog>]

#  we cal also narrow these searches using filters 

#  with app.app_context():
#     Owner.query.filter(Owner.name >= 'Ben').all()


# Serving database records in fask apps 
    

