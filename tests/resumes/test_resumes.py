from tests.conftest import register_and_login


async def test_create_resume(ac):
    headers = await register_and_login(ac)

    response = await ac.post(
        "/resumes",
        json={"title": "Test resume", "content": "Some content"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test resume"
    assert data["content"] == "Some content"
    assert "id" in data


async def test_get_user_resume(ac):
    headers = await register_and_login(ac)

    response = await ac.get("/resumes/me", headers=headers)

    assert response.status_code == 200


async def test_get_resume(ac):
    headers = await register_and_login(ac)

    response = await ac.get(f"/resumes/{1}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test resume"


async def test_update_resume(ac):
    headers = await register_and_login(ac)

    response = await ac.patch(
        f"/resumes/{1}",
        json={"title": "test update", "content": "test update"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "test update"


async def test_improve_resume(ac):
    headers = await register_and_login(ac)

    response = await ac.patch(f"/resumes/{1}/improve", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data == "test update Improved"


async def test_delete_resume(ac):
    headers = await register_and_login(ac)

    response = await ac.delete(f"/resumes/{1}", headers=headers)
    assert response.status_code == 200
    # data = response.json()
    # print(data)
    # assert data == "test update Improved"
