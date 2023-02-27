#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False

migrate = Migrate(app, db)

db.init_app(app)


def serialize_bakery(bakery):
    return {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at
    }


def serialize_baked_good(baked_good):
    return {
        "id": baked_good.id,
        "name": baked_good.name,
        "price": baked_good.price,
        "created_at": baked_good.created_at,
        "updated_at": baked_good.updated_at
    }


@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


@app.route('/bakeries')
def get_bakeries():
    bakeries = [serialize_bakery(bakery) for bakery in Bakery.query.all()]
    return jsonify(bakeries)


@app.route('/bakeries/<int:bakery_id>')
def get_bakery(bakery_id):
    bakery = Bakery.query.get_or_404(bakery_id)
    return jsonify(serialize_bakery(bakery))


@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = [serialize_baked_good(baked_good) for baked_good in BakedGood.query.order_by(desc(BakedGood.price))]
    return jsonify(baked_goods)


@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first_or_404()
    return jsonify(serialize_baked_good(baked_good))


if __name__ == '__main__':
    app.run(port=5555, debug=True)
