from flask import Flask, jsonify, request
from orm import inventory
from db import Database


app=Flask(__name__)

db = Database()

@app.route("/inventory",methods=["GET"])
def list_inventory():
    inventory_store = inventory(db)
    items = inventory_store.get_all_items()
    return jsonify(items)

@app.route("/inventory",methods=["POST"])
def add_inventory():
    data=request.get_json()
    
    new_item=inventory.add_item(data["name"],
                                data["qty"],
                                data["buying_price"],data["selling_price"])
    return jsonify({"message":"Item added successfully","item":new_item}),201

#jdjfke
if __name__=="__main__":
    app.run(debug=True)