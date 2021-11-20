import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    # print(res.json())
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/0980")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_user, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

    user = schemas.UserResponseData(**test_user)
    post = schemas.PostResponseData(owner = user, **res.json()['data'])

    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
    assert post.owner_id == str(test_user['id'])
    assert post.owner_id == str(test_posts[0].owner_id)


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favourite dish", "i love tacos", False),
    ("tallest build", "burj", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts", json={"title": title, "content": content, "published": published})
    
    created_post = schemas.PostResponse(**res.json()).data
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == str(test_user['id'])


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts", json={"title": "title", "content": "content"})
    
    created_post = schemas.PostResponse(**res.json()).data
    
    assert res.status_code == 201
    assert created_post.published == True


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts", json={"title": "title", "content": "content"})
    
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/9090")
    
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    
    assert res.status_code == 403


def test_update_posts(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.PostResponse(**res.json()).data
    assert res.status_code == 205
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user_2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    updated_post = schemas.PostResponse(**res.json()).data
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/9090", json=data)
    
    assert res.status_code == 404