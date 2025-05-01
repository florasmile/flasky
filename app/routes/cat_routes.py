from flask import Blueprint, abort, make_response, request, Response
from sqlalchemy import or_
from ..db import db
from app.models.cat import Cat
from .route_utilities import validate_model

cats_bp = Blueprint("cats_bp", __name__, url_prefix = "/cats")

@cats_bp.post("")
def create_cat():
    request_body = request.get_json()
    new_cat = Cat.from_dict(request_body)

    db.session.add(new_cat)
    db.session.commit()

    return new_cat.to_dict(), 201

@cats_bp.get("")
def get_all_cats():
    query = db.select(Cat)
    name_param = request.args.get("name")
    if name_param:
        query = query.where(
            Cat.name == name_param
            )
    color_param = request.args.get("color")
    if color_param:
        query = query.where(
             or_(
                 Cat.color.ilike(f"%{color_param}%")
                 )
        )

    query = query.order_by(Cat.id)

    cats = db.session.scalars(query)

    cats_response = []

    for cat in cats:
        cats_response.append(
            cat.to_dict()
        )
    return cats_response

@cats_bp.get("/<id>")
def get_one_cat(id):
    cat = validate_model(Cat, id)

    return cat.to_dict()


@cats_bp.put("/<id>")
def update_cat(id):
    cat = validate_model(Cat, id)

    request_body = request.get_json() 

    cat.name = request_body["name"]
    cat.color = request_body["color"]
    cat.personality = request_body["personality"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@cats_bp.delete("/<id>")
def delete_cat(id):
    cat = validate_model(Cat, id)

    db.session.delete(cat)

    db.session.commit()

    return Response(status=204, mimetype="application/json")




# def get_all_cats():
#     results_list = []
#     for cat in cats:
#         results_list.append(dict(
#             id = cat.id,
#             name = cat.name,
#             color = cat.color,
#             personality = cat.personality
#         ))
#     return results_list



        
        



