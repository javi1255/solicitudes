from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    full_name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Solicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_solicitud = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/Mexico_City')))
    nombre_completo = db.Column(db.String(128))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    comunidad = db.Column(db.String(128))
    fuente = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.String(20), default='Pendiente')
    dias_sin_resolver = db.Column(db.Integer, default=0)
    monto_solicitado = db.Column(db.Float)
    monto_aprobado = db.Column(db.Float)
    realizado_por = db.Column(db.String(128))
    foto1 = db.Column(db.String(200), nullable=True)
    foto2 = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('solicitudes', lazy=True))

    def actualizar_dias_sin_resolver(self):
        now = datetime.now(pytz.timezone('America/Mexico_City'))
        if self.fecha_solicitud.tzinfo is None:
            self.fecha_solicitud = pytz.timezone('America/Mexico_City').localize(self.fecha_solicitud)
        delta = now - self.fecha_solicitud
        self.dias_sin_resolver = delta.days