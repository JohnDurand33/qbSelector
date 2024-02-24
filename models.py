from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True, default='')
    last_name = db.Column(db.String(100), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password, first_name='', last_name='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.first_name = first_name or ''
        self.last_name = last_name or ''
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'<User | id: {self.id} | email: {self.email}>'


class Quarterback(db.Model):
    __tablename__ = 'quarterback'
    id = db.Column(db.String, primary_key=True)
    team = db.Column(db.String(50))
    division = db.Column(db.String(10))
    conference = db.Column(db.String(50))
    image_link = db.Column(db.String(256), nullable=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,team,division= '',conference='',image_link='',user_token=''):
        self.id = self.set_id()
        self.team = team
        self.division = division
        self.conference = conference
        self.image_link = image_link
        self.user_token = user_token

    def __repr__(self):
        return f'<Quarterback | Team: {self.team} | Division: {self.division} | Conference: {self.conference}>'

    def set_id(self):
        return (secrets.token_urlsafe())

class QuarterbackSchema(ma.Schema):
    class Meta:
        fields = ['id', 'team','division','conference', 'image_link']

qb_schema = QuarterbackSchema()
qbs_schema = QuarterbackSchema(many=True)