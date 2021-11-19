import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alembic import command

from app.main import app
from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app import models

# SQLA = 'postgresql://<username>:<password>@<ip-address/hostname>:<port>/<database_name>'
SQLACHEMY_DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test'

engine = create_engine(SQLACHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    email = "hello@gmail.com"
    user_data = {
        "email": email,
        "password": "1234"
    }
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()['data']
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user_2(client):
    email = "hello23@gmail.com"
    user_data = {
        "email": email,
        "password": "1234"
    }
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()['data']
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f'Bearer {token}'
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user_2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id']
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user['id']
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user_2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts