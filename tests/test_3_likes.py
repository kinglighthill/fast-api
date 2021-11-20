import pytest
from app import models

@pytest.fixture()
def test_like(test_posts, session, test_user):
    new_like = models.Like(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_like_on_post(authorized_client, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "like": True,
    }
    res = authorized_client.post("/like", json=data)
    assert res.status_code == 201
    
def test_like_twice_post(authorized_client, test_posts, test_like):
    data = {
        "post_id": test_posts[3].id,
        "like": True,
    }
    res = authorized_client.post("/like", json=data)
    assert res.status_code == 409

def test_delete_like(authorized_client, test_posts, test_like):
    data = {
        "post_id": test_posts[3].id,
        "like": False,
    }
    res = authorized_client.post("/like", json=data)
    assert res.status_code == 201

def test_delete_like_non_exist(authorized_client, test_posts):
    data = {
        "post_id": test_posts[3].id,
        "like": False,
    }
    res = authorized_client.post("/like", json=data)
    assert res.status_code == 404

def test_like_non_exist(authorized_client, test_posts):
    data = {
        "post_id": 98,
        "like": False,
    }
    res = authorized_client.post("/like", json=data)
    assert res.status_code == 404

def test_like_unauthorized_use(client, test_posts):
    data = {
        "post_id": test_posts[3].id,
        "like": False,
    }
    res = client.post("/like", json=data)
    assert res.status_code == 401