# import pytest
# from fastapi_neon.main import app
# from starlette.testclient import TestClient
# from unittest.mock import MagicMock
# from sqlalchemy import select
# from fastapi_neon.main import TodoRead, get_session, Todo

# @pytest.fixture
# def client():
#     with TestClient(app) as test_client:
#         yield test_client

# def test_read_todos_with_default_offset_and_limit(client):
#     # Mock the get_session function to return a session
#     session_mock = MagicMock()
#     session_mock.exec.return_value.all.return_value = [Todo(id=1, content="Todo 1")]
#     get_session_mock = MagicMock(return_value=session_mock)

#     app.dependency_overrides[get_session] = get_session_mock

#     # Call the read_todos endpoint without specifying offset and limit
#     response = client.get("/todos/")

#     # Check if the endpoint returned a successful response
#     assert response.status_code == 200

#     # Check if the mocked session's exec method was called with the correct arguments
#     session_mock.exec.assert_called_once_with(select(Todo).offset(0).limit(10))

#     # Check if the response contains the expected todos
#     assert response.json() == [{"id": 1, "content": "Todo 1"}]

# def test_read_todos_with_custom_offset_and_limit(client):
#     # Mock the get_session function to return a session
#     session_mock = MagicMock()
#     session_mock.exec.return_value.all.return_value = [Todo(id=1, content="Todo 1")]
#     get_session_mock = MagicMock(return_value=session_mock)

#     app.dependency_overrides[get_session] = get_session_mock

#     # Call the read_todos endpoint with custom offset and limit
#     response = client.get("/todos/?offset=5&limit=15")

#     # Check if the endpoint returned a successful response
#     assert response.status_code == 200

#     # Check if the mocked session's exec method was called with the correct arguments
#     session_mock.exec.assert_called_once_with(select(Todo).offset(5).limit(15))

#     # Check if the response contains the expected todos
#     assert response.json() == [{"id": 1, "content": "Todo 1"}]

# def test_create_todo_success(client):
#     # Test creation of a todo
#     response = client.post("/todos/", json={"content": "Test Todo"})
#     assert response.status_code == 200







# def test_create_todo_success(client):
#     todo_data = {"content": "Test Todo"}
#     response = client.post("/todos/", json=todo_data)
#     assert response.status_code == 200
#     assert response.json()["content"] == "Test Todo"
#     assert "id" in response.json()


# def test_create_todo_invalid_data(client):
#     todo_data = {"invalid_key": "Test Todo"}
#     response = client.post("/todos/", json=todo_data)
#     assert response.status_code == 422  # Unprocessable Entity


# @contextmanager
# def get_session():
#     session = session(engine)
#     try:
#         yield session
#     finally:
    #     session.close()def test_get_session():
    # with get_session() as session:
    #     assert session is not None

# def test_todo_model():
#     todo = Todo(content="Test Todo")
#     assert todo.content == "Test Todo"




    