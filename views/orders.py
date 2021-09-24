from flask import Blueprint, render_template
from common.forms import NewOrder
from models.user.decorators import require_login


order_blueprint = Blueprint('orders', __name__)


@order_blueprint.route('/', methods=['GET', 'POST'])
@require_login
def new_order():
    form = NewOrder()
    return render_template('orders/new.html', form=form)
