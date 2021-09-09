from functools import partial
from flask import Blueprint, render_template, redirect, url_for, flash, session

from common.forms import NewUser
from models import User
from models.user.errors import UserError
from common.flash_message import register_success
from common.generate_many_flash_message import generate_many_flash_message


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def new_user():
    form = NewUser()
    flash_warning_messages = partial(generate_many_flash_message, category='warning')

    if form.validate_on_submit():
        try:
            User.register(
                display_name=form.display_name.data,
                email=form.email.data,
                password=form.password.data,
                cell_phone=form.cell_phone.data,
                address=form.address.data,
                store_introduction=form.store_introduction.data
            )

            user = User.find_by_email(form.email.data)
            session['user'] = user.json()
            flash(*register_success)
            return redirect(url_for('home'))

        except UserError as e:
            flash_warning_messages([e.message])

    else:
        flash_warning_messages(form.display_name.errors)
        flash_warning_messages(form.email.errors)
        flash_warning_messages(form.password.errors)
        flash_warning_messages(form.confirm_password.errors)
        flash_warning_messages(form.cell_phone.errors)
        flash_warning_messages(form.address.errors)
        flash_warning_messages(form.store_introduction.errors)

    return render_template('users/new.html', form=form)
