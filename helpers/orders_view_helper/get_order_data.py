from datetime import datetime
from models import Order, OrderItem, OrderStatus, PaymentStatus, ShippingStatus


def get_order_data(order_id, user_id):
    row = Order.query \
        .with_entities(Order, OrderItem, OrderStatus, PaymentStatus, ShippingStatus) \
        .join(OrderItem) \
        .join(OrderStatus) \
        .join(PaymentStatus) \
        .join(ShippingStatus) \
        .filter(Order.id == order_id) \
        .filter((Order.buyer_id == user_id) | (Order.seller_id == user_id)) \
        .all()

    if not row:
        return None

    order = {
        'id': row[0].Order.id,
        'amount': f'{row[0].Order.amount:,}',
        'amount_int': row[0].Order.amount,
        'recipient': row[0].Order.recipient,
        'cell_phone': row[0].Order.cell_phone,
        'address': row[0].Order.address,
        'insert_time': datetime.strftime(row[0].Order.insert_time, '%Y-%m-%d'),
        'update_time': datetime.strftime(row[0].Order.update_time, '%Y-%m-%d'),
        'buyer_id': row[0].Order.buyer_id,
        'order_status_id': row[0].OrderStatus.id,
        'order_status': row[0].OrderStatus.status,
        'payment_status_id': row[0].PaymentStatus.id,
        'payment_status': row[0].PaymentStatus.status,
        'shipping_status_id': row[0].ShippingStatus.id,
        'shipping_status': row[0].ShippingStatus.status,
        'order_items': []
    }
    for data in row:
        order['order_items'].append({
            'image_url': data.OrderItem.image_url,
            'name': data.OrderItem.name,
            'price': f'{data.OrderItem.price:,}',
            'quantity': data.OrderItem.quantity,
            'subtotal': f'{data.OrderItem.price * data.OrderItem.quantity:,}'
        })

    return order
