from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, FloatField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed

class FormularioLogin(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class FormularioRegistro(FlaskForm):
    full_name = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class FormularioSolicitud(FlaskForm):
    nombre_completo = StringField('Nombre Completo', validators=[DataRequired()])
    telefono = StringField('Número de Teléfono', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    comunidad = StringField('Comunidad', validators=[DataRequired()])
    fuente = SelectField('Fuente', choices=[('Directa', 'Directa'), ('Redes Sociales', 'Redes Sociales'), ('Oficio', 'Oficio'), ('Llamada Telefónica', 'Llamada Telefónica')], validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    estatus = SelectField('Estatus', choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Completado', 'Completado')], validators=[DataRequired()])
    monto_solicitado = FloatField('Monto Solicitado', validators=[DataRequired()])
    monto_aprobado = FloatField('Monto Aprobado', validators=[DataRequired()])
    realizado_por = StringField('Realizado por', validators=[DataRequired()])
    foto1 = FileField('Foto 1', validators=[FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes!')])
    foto2 = FileField('Foto 2', validators=[FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes!')])
    submit = SubmitField('Crear Solicitud')