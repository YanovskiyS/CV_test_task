from tests.conftest import register_and_login


async def test_create_resume(ac):
    headers = await register_and_login(ac)

    response = await ac.post(
        "/resumes",
        json={"title": "Test resume", "content": "Some content"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test resume"
    assert data["content"] == "Some content"
    assert "id" in data

