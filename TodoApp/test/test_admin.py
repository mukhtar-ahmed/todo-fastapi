from .utils import *
from ..routers.admin import get_db,get_current_user
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK

def test_admin_delete_todo(test_todo):
    response = client.delete(f"/admin/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_admin_delete_todo_not_found(test_todo):
    response = client.delete(f"/admin/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

