from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    person_favorites = db.relationship('Person', secondary="person_favorite", back_populates='favorited_by_users')
    planet_favorites = db.relationship('Planet', secondary="planet_favorite", back_populates='planet_favorited_by_users')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    height = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    favorited_by_users = db.relationship('User', secondary="person_favorite", back_populates='person_favorites')

    def serialize(self):
        return {
            "id": self.id,
            "birth_year": self.birth_year,
            "name": self.name,
            "height": self.height,
            "description": self.description,
        }
    
    def __repr__(self):
        return '<Person %r>' % self.name

class PersonFavorite(db.Model):
    __tablename__ = 'person_favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id
        } 

    def __repr__(self):
        return f'<PersonFavorite user_id={self.user_id} person_id={self.person_id}>'
    

class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    planet_favorited_by_users = db.relationship('User', secondary="planet_favorite", back_populates='planet_favorites')


    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            "name": self.name,
            "population": self.population,
            "description": self.description,
        }
    
    def __repr__(self):
        return '<Planet %r>' % self.name
    
class PlanetFavorite(db.Model):
    __tablename__ = 'planet_favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        } 

    def __repr__(self):
        return f'<PlanetFavorite user_id={self.user_id} planet_id={self.planet.id}>'