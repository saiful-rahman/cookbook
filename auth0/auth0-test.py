import requests

DOMAIN = 'dev-aoojpnwcqsr11uc1.uk.auth0.com'
CLIENT_ID = 'TJ0Qv9mrw5eqFM9GBVSWIiazFKcbmV70'
CLIENT_SECRET = 'IOdSmVgj68JGGuQt0H0FLV-jqNvUKbYTqPzotOFaIh0-QdVihOCIll6yHHgh0p4T'

USERNAME = 'a@b.com'
PASSWORD = 'Test@1234'
AUDIENCE = 'https://test/api'
GRANT_TYPE = 'password'

url = 'https://dev-aoojpnwcqsr11uc1.uk.auth0.com/oauth/token'
payload = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'username': USERNAME,
    'password': PASSWORD,
    'audience': AUDIENCE,
    'grant_type': GRANT_TYPE
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    response_json = response.json()
    access_token = response_json.get('access_token')
    print(access_token)
else:
    print(f"failed: status-code:{response.status_code}, error-text:{response.text}")
