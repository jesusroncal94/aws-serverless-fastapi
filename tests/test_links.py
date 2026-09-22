TARGET_URL = "https://example.com/documentation"


async def test_health_reports_ok(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_shortened_link_redirects_and_counts_the_visit(client):
    created = await client.post("/links", json={"target_url": TARGET_URL})

    assert created.status_code == 201
    link = created.json()
    assert link["target_url"] == TARGET_URL
    assert link["visits"] == 0
    assert link["short_url"] == f"http://testserver/{link['code']}"

    redirect = await client.get(f"/{link['code']}")

    assert redirect.status_code == 307
    assert redirect.headers["location"] == TARGET_URL

    stats = await client.get(f"/links/{link['code']}")

    assert stats.status_code == 200
    assert stats.json()["visits"] == 1


async def test_unknown_code_is_not_found(client):
    response = await client.get("/missing")

    assert response.status_code == 404
