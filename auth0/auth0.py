import typer
import requests

DOMAIN = 'dev-aoojpnwcqsr11uc1.uk.auth0.com'
CLIENT_ID = 'TJ0Qv9mrw5eqFM9GBVSWIiazFKcbmV70'
CLIENT_SECRET = 'IOdSmVgj68JGGuQt0H0FLV-jqNvUKbYTqPzotOFaIh0-QdVihOCIll6yHHgh0p4T'
GRANT_TYPE = 'password'

app = typer.Typer()


def post_oauth_token(payload: dict):

    url = f"https://{DOMAIN}/oauth/token"
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get('access_token')
        print(access_token)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


# python3 auth0/auth0.py get-access-token 'https://test/api' 'a@b.com' 'password'
@app.command()
def get_access_token(audience: str, username: str, password: str):

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'username': username,
        'password': password,
        'audience': audience,
        'grant_type': GRANT_TYPE
    }

    post_oauth_token(payload)


# python3 auth0/auth0.py oauth-token 'https://saif/api
@app.command()
def oauth_token(audience: str):

    C_ID = "ExuqYdxKcF2bcjHHrv3aqS0R470BtGu5"
    C_SECRET = "G9ZfvzXqq4ziTosCpb-r-WmLDJWuMWka4WWHp4yXyBOia2nkpxZOHIjNesOfDd1f"

    payload = {
        'client_id': C_ID,
        'client_secret': C_SECRET,
        'audience': audience,
        'grant_type': 'client_credentials'
    }

    post_oauth_token(payload)


if __name__ == "__main__":
    app()
