from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/pokemonwebsite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

teams = db.Table(
    'teams',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)                                                 
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=True)  # Increase the length here
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    team_pokemons = db.relationship(
        'Pokemon', secondary=teams, 
        back_populates='trainers', 
        lazy='dynamic'
    )

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

    def can_add_pokemon_to_team(self):
        return len(list(self.team_pokemons)) < 5  


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  
    sprite_url = db.Column(db.String(100), nullable=False)  
    attack_base_stat = db.Column(db.Integer)
    base_experience = db.Column(db.Integer)
    hp_base_stat = db.Column(db.Integer)
    defense_base_stat = db.Column(db.Integer)
    ability_name = db.Column(db.String(100))
    trainers = db.relationship(
        'User', 
        secondary=teams, 
        back_populates='team_pokemons',
        lazy='dynamic'
    )
        
    def __init__(self, name, sprite_url, attack_base_stat, base_experience, hp_base_stat, defense_base_stat, ability_name):
        self.name = name
        self.sprite_url = sprite_url
        self.attack_base_stat = attack_base_stat
        self.base_experience = base_experience 
        self.hp_base_stat = hp_base_stat
        self.defense_base_stat = defense_base_stat
        self.ability_name = ability_name

with app.app_context():
    db.create_all()
