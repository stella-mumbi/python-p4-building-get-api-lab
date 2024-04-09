from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "created_at": bakery.created_at,
            "name": bakery.name,
            "baked_goods": []  # Initialize an empty list for baked goods
        }

        # Populate the baked goods for the current bakery
        for baked_good in bakery.baked_goods:
            baked_good_dict = {
                "baked_good_id": baked_good.id,
                "name": baked_good.name,
                "price": baked_good.price,
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
            }
            bakery_dict["baked_goods"].append(baked_good_dict)

        bakeries_list.append(bakery_dict)

    return jsonify(bakeries_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if bakery:
        bakery_dict = {
            "id": bakery.id,
            "created_at": bakery.created_at,
            "name": bakery.name,
            "baked_goods": []  # Initialize an empty list for baked goods
        }

        # Populate the baked goods for the current bakery
        for baked_good in bakery.baked_goods:
            baked_good_dict = {
                "baked_good_id": baked_good.id,
                "name": baked_good.name,
                "price": baked_good.price,
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
            }
            bakery_dict["baked_goods"].append(baked_good_dict)

        return jsonify(bakery_dict), 200
    else:
        return jsonify({"error": f"Bakery with id {id} not found"}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_list = []

    # Query baked goods sorted by price in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    for baked_good in baked_goods:
        baked_good_dict = {
            "bakery": {
                "created_at": baked_good.bakery.created_at,
                "id": baked_good.bakery.id,
                "name": baked_good.bakery.name,
                "updated_at": baked_good.bakery.updated_at,
            },
            "bakery_id": baked_good.bakery_id,
            "created_at": baked_good.created_at,
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "updated_at": baked_good.updated_at,
        }
        baked_goods_list.append(baked_good_dict)

    response = make_response(jsonify(baked_goods_list), 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive:
        most_expensive_dict = {
            "bakery": {
                "created_at": most_expensive.bakery.created_at,
                "id": most_expensive.bakery.id,
                "name": most_expensive.bakery.name,
                "updated_at": most_expensive.bakery.updated_at,
            },
            "bakery_id": most_expensive.bakery_id,
            "created_at": most_expensive.created_at,
            "id": most_expensive.id,
            "name": most_expensive.name,
            "price": most_expensive.price,
            "updated_at": most_expensive.updated_at,
        }

        response = make_response(jsonify(most_expensive_dict), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        return jsonify({"error": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
