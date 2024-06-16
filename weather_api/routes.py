from flask import Blueprint, request, jsonify
from .models import db, Subscriber

api = Blueprint('api', __name__)

@api.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')
    frequency = data.get('frequency')

    if not email or not frequency:
        return jsonify({'error': 'Email and frequency are required'}), 400

    if frequency not in ['weekly', 'biweekly', 'monthly', 'semiannual']:
        return jsonify({'error': 'Invalid frequency value'}), 400

    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber:
        return jsonify({'error': 'Email is already subscribed'}), 400

    new_subscriber = Subscriber(email=email, frequency=frequency)
    db.session.add(new_subscriber)
    db.session.commit()

    return jsonify({'message': 'Subscribed successfully'}), 201

@api.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    subscriber = Subscriber.query.filter_by(email=email).first()
    if not subscriber:
        return jsonify({'error': 'Email is not subscribed'}), 400

    db.session.delete(subscriber)
    db.session.commit()

    return jsonify({'message': 'Unsubscribed successfully'}), 200
