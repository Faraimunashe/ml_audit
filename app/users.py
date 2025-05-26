from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app.models import User
from app.forms import UserForm
from . import db
from app.audit_helper import log_create, log_update, log_delete
from passlib.hash import sha256_crypt

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@users_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Error email already exists!')
            return redirect(url_for('users.users'))
        
        password = form.password.data
        passwordata = sha256_crypt.encrypt(password)
        user = User(
            email=form.email.data,
            password=passwordata,
            name=form.name.data,
            role=int(form.role.data)
        )
        db.session.add(user)
        db.session.commit()

        log_create(user)

        flash('User created successfully', 'success')
        return redirect(url_for('users.users'))
    return render_template('create.html', form=form)


@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)

    form.password.validators = []
    form.confirm_password.validators = []

    old_data = user.to_dict()

    if form.validate_on_submit():
        user.email = form.email.data
        user.name = form.name.data
        user.role = int(form.role.data)

        if form.password.data:
            password = form.password.data
            passwordata = sha256_crypt.encrypt(password)
            user.password = passwordata

        db.session.commit()
        log_update(user, old_data)

        flash('User updated successfully', 'success')
        return redirect(url_for('users.users'))
    return render_template('edit.html', form=form, user=user)


@users_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete(user_id):
    user = User.query.get_or_404(user_id)
    log_delete(user) 
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('users.users'))
