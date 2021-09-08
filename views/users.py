from flask import Blueprint, render_template
from common.forms import NewUser


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def new_user():
    form = NewUser()

    return render_template('users/new.html', form=form)
