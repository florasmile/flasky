from app.db import db
from app.models.cat import Cat

def test_get_all_cats_returns_empty_list_when_db_is_empty(client):
    #act
    response = client.get("/cats")

    #assert
    assert response.status_code == 200
    assert response.get_json() == []
  
def test_get_one_cat_returns_seeded_cat(client, one_cat):
    # act
    response = client.get(f"/cats/{one_cat.id}")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body["id"] == one_cat.id
    assert response_body["name"] == one_cat.name
    assert response_body["color"] == one_cat.color
    assert response_body["personality"] == one_cat.personality


def test_create_cat_happy_path(client):
    # arrange
    EXPECTED_CAT = {
        "name": "Luna",
        "color": "orange",
        "personality": "cute"
    }
    # act
    response = client.post("/cats", json=EXPECTED_CAT)
    response_body = response.get_json()
  
    # assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["name"] == EXPECTED_CAT["name"]
    assert response_body["color"] == EXPECTED_CAT["color"]
    assert response_body["personality"] == EXPECTED_CAT["personality"]

    # further check that the DB was actually updated
    query = db.select(Cat).where(Cat.id == 1)
    new_cat = db.session.scalar(query) # compare values to expected

    assert new_cat.id == 1
    assert new_cat.name == EXPECTED_CAT["name"]
    assert new_cat.color == EXPECTED_CAT["color"]
    assert new_cat.personality == EXPECTED_CAT["personality"]