import os
from datetime import datetime
import pytz
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app.models import User, Solicitud
from app import db
from app.forms import FormularioLogin, FormularioRegistro, FormularioSolicitud

bp = Blueprint('main', __name__)

def save_picture(form_picture):
    random_hex = os.urandom(8).hex()
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(bp.root_path, 'static/fotos', picture_fn)
    
    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    form_picture.save(picture_path)
    return picture_fn

@bp.route('/')
@bp.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if current_user.is_authenticated:
        return redirect(url_for('main.panel'))
    form = FormularioLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos')
            return redirect(url_for('main.inicio_sesion'))
        login_user(user)
        return redirect(url_for('main.panel'))
    return render_template('inicio_sesion.html', title='Iniciar Sesión', form=form)

@bp.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    return redirect(url_for('main.inicio_sesion'))

@bp.route('/panel')
@login_required
def panel():
    solicitudes = Solicitud.query.filter(Solicitud.estatus.in_(['Pendiente', 'En Proceso'])).all()
    for solicitud in solicitudes:
        solicitud.actualizar_dias_sin_resolver()
    db.session.commit()
    return render_template('panel.html', title='Panel de Control', solicitudes=solicitudes)

@bp.route('/solicitudes_atendidas')
@login_required
def solicitudes_atendidas():
    solicitudes = Solicitud.query.filter_by(estatus='Atendida').all()
    return render_template('solicitudes_atendidas.html', title='Solicitudes Atendidas', solicitudes=solicitudes)

@bp.route('/solicitudes_rechazadas')
@login_required
def solicitudes_rechazadas():
    solicitudes = Solicitud.query.filter_by(estatus='Rechazada').all()
    return render_template('solicitudes_rechazadas.html', title='Solicitudes Rechazadas', solicitudes=solicitudes)

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.panel'))
    form = FormularioRegistro()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, full_name=form.full_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Felicidades, ahora eres un usuario registrado!')
        return redirect(url_for('main.inicio_sesion'))
    return render_template('registro.html', title='Registro', form=form)

@bp.route('/nueva_solicitud', methods=['GET', 'POST'])
@login_required
def nueva_solicitud():
    form = FormularioSolicitud()
    if form.validate_on_submit():
        foto1_file = save_picture(form.foto1.data) if form.foto1.data else None
        foto2_file = save_picture(form.foto2.data) if form.foto2.data else None
        solicitud = Solicitud(
            nombre_completo=form.nombre_completo.data,
            telefono=form.telefono.data,
            email=form.email.data,
            comunidad=form.comunidad.data,
            fuente=form.fuente.data,
            descripcion=form.descripcion.data,
            estatus=form.estatus.data,
            monto_solicitado=form.monto_solicitado.data,
            monto_aprobado=form.monto_aprobado.data,
            realizado_por=form.realizado_por.data,
            foto1=foto1_file,
            foto2=foto2_file,
            user_id=current_user.id
        )
        db.session.add(solicitud)
        db.session.commit()
        flash('¡Nueva solicitud creada!')
        return redirect(url_for('main.panel'))
    return render_template('nueva_solicitud.html', title='Nueva Solicitud', form=form)

@bp.route('/editar_solicitud/<int:solicitud_id>', methods=['GET', 'POST'])
@login_required
def editar_solicitud(solicitud_id):
    solicitud = Solicitud.query.get_or_404(solicitud_id)
    form = FormularioSolicitud(obj=solicitud)
    if form.validate_on_submit():
        solicitud.nombre_completo = form.nombre_completo.data
        solicitud.telefono = form.telefono.data
        solicitud.email = form.email.data
        solicitud.comunidad = form.comunidad.data
        solicitud.fuente = form.fuente.data
        solicitud.descripcion = form.descripcion.data
        solicitud.estatus = form.estatus.data
        solicitud.monto_solicitado = form.monto_solicitado.data
        solicitud.monto_aprobado = form.monto_aprobado.data
        solicitud.realizado_por = form.realizado_por.data
        if form.foto1.data:
            solicitud.foto1 = save_picture(form.foto1.data)
        if form.foto2.data:
            solicitud.foto2 = save_picture(form.foto2.data)
        db.session.commit()
        flash('¡Solicitud actualizada!')
        return redirect(url_for('main.panel'))
    return render_template('nueva_solicitud.html', title='Editar Solicitud', form=form)

@bp.route('/eliminar_solicitud/<int:solicitud_id>', methods=['POST'])
@login_required
def eliminar_solicitud(solicitud_id):
    solicitud = Solicitud.query.get_or_404(solicitud_id)
    db.session.delete(solicitud)
    db.session.commit()
    flash('¡Solicitud eliminada!')
    return redirect(url_for('main.panel'))

@bp.route('/reporte_solicitud/<int:solicitud_id>', methods=['GET'])
@login_required
def reporte_solicitud(solicitud_id):
    solicitud = Solicitud.query.get_or_404(solicitud_id)
    return render_template('reporte_solicitud.html', title='Reporte de Solicitud', solicitud=solicitud)

@bp.route('/aprobar_solicitud/<int:solicitud_id>', methods=['POST'])
@login_required
def aprobar_solicitud(solicitud_id):
    solicitud = Solicitud.query.get_or_404(solicitud_id)
    solicitud.estatus = 'Atendida'
    db.session.commit()
    flash('¡Solicitud aprobada!')
    return redirect(url_for('main.panel'))

@bp.route('/rechazar_solicitud/<int:solicitud_id>', methods=['POST'])
@login_required
def rechazar_solicitud(solicitud_id):
    solicitud = Solicitud.query.get_or_404(solicitud_id)
    solicitud.estatus = 'Rechazada'
    db.session.commit()
    flash('¡Solicitud rechazada!')
    return redirect(url_for('main.panel'))

@bp.route('/marcador', methods=['GET'])
@login_required
def marcador():
    total_rechazadas = Solicitud.query.filter_by(estatus='Rechazada').count()
    total_aprobadas = Solicitud.query.filter_by(estatus='Atendida').count()
    total_pendientes = Solicitud.query.filter(Solicitud.estatus.in_(['Pendiente', 'En Proceso'])).count()
    return jsonify({
        'total_rechazadas': total_rechazadas,
        'total_aprobadas': total_aprobadas,
        'total_pendientes': total_pendientes
    })

@bp.route('/ver_marcador')
@login_required
def ver_marcador():
    return render_template('marcador.html', title='Marcador de Solicitudes')