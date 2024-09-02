from ..routers.todos import get_db,get_current_user
from fastapi import status
from ..models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title": "its for test",
        "description": "gescription for test",
        "priority": 1,
        "complete": False,
        "owner_id": 1,
        "id": 1
    }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": "its for test",
        "description": "gescription for test",
        "priority": 1,
        "complete": False,
        "owner_id": 1,
        "id": 1
    }

def test_read_one_not_found(test_todo):
    response = client.get("/todo/99")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_todo(test_todo):
    request_data = {
        "title": "its for test",
        "description": "gescription for test",
        "priority": 1,
        "complete": False,
    }
    response = client.post("/todos/todo/",json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")

def test_updated_todo(test_todo):
    request_data = {
        "title": "Change Titleits for test",
        "description": "gescription for test",
        "priority": 5,
        "complete": False,
    }
    response = client.put("/todos/todo/1",json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Change Titleits for test'

def test_updated_todo_not_found(test_todo):
    request_data = {
        "title": "Change Titleits for test",
        "description": "gescription for test",
        "priority": 5,
        "complete": False,
    }
    response = client.put("/todos/todo/999",json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todos/todo/999')
    assert response.status_code == 404
    
