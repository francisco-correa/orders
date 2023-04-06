from flask import Flask, jsonify, abort, request

app = Flask(__name__)

orders = [{"id": 1,
           "sku": 123,
           "product": "camisa",
           "quantity": 1,
           "price": 30},
          {"id": 2,
           "sku": 345,
           "product": "pantalones",
           "quantity": 2,
           "price": 60},
          {"id": 3,
           "sku": 678,
           "product": "zapatos",
           "quantity": 1,
           "price": 25}]


@app.route('/')
def index():
    return 'Welcome to the orders page, please add /orders to start a new project after the port number'


@app.route('/orders', methods=["GET"])
def get_orders():
    return jsonify({"orders": orders})


@app.route('/orders/<int:order_id>', methods=["GET"])
def get_order(order_id):
    order = [order for order in orders if order["id"] == order_id]
    if len(order) == 0:
        abort(404, description="You dont get the right order_id, try again")
    return jsonify({"order": order[0]})


@app.route('/orders/', methods=["POST"])
def create_order():
    if not request.json or not "product" in request.json:
        abort(400, description="Yo cant create orders, review your JSON AGAIN")
    order = {"id": orders[-1]["id"] + 1,
             "product": request.json["product"],
             "quantity": request.json.get("quantity"),
             "price": request.json.get("price"),
             "sku": request.json.get("sku")
             }
    orders.append(order)
    return jsonify({"order": order}), 201


@app.route('/orders/<int:order_id>', methods=["PUT"])
def update_order(order_id):
    order = [order for order in orders if order["id"] == order_id]
    if len(order) == 0:
        abort(404, description="You dont get the right order_id, try again")
    if not request.json:
        abort(400)
    order[0]["product"] = request.json.get("product", order[0]["product"])
    order[0]["quantity"] = request.json.get("quantity", order[0]["quantity"])
    order[0]["price"] = request.json.get("price", order[0]["price"])
    return jsonify({"order": order[0]})


@app.route('/orders/<int:order_id>', methods=["DELETE"])
def delete_order(order_id):
    order = [order for order in orders if order["id"] == order_id]
    if len(order) == 0:
        abort(404, description="You dont get the right order_id, try again")
    orders.remove(order[0])
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
