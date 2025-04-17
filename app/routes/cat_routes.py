from flask import Blueprint
from ..models.cat import cats
cats_bp = Blueprint("cats_bp", __name__, url_prefix = "/cats")

@cats_bp.get("/")
def get_all_cats():
    results_list = []
    for cat in cats:
        results_list.append(dict(
            id = cat.id,
            name = cat.name,
            color = cat.color,
            personality = cat.personality
        ))
    return results_list
          
        
        

@cats_bp.get("/<id>")
def get_one_cat(id):
    pass