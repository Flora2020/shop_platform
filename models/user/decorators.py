from functools import wraps
from typing import Callable
from flask import session, flash, redirect, url_for
from common.flash_message import login_required_msg


def require_login(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            flash(*login_required_msg)
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)

    return decorated_function
