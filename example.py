import httpx

response = httpx.get(
    url="http://localhost:80/",
    timeout=30,
)
print(response.status_code)
print(response.text)


response = httpx.post(
    url="http://localhost:80/scrape/",
    json={
        "page_limit": 2,
    },
    headers={
        "Authorization": "Bearer 1234567890"
    },
    timeout=30,
)
print(response.status_code)
print(response.text)
