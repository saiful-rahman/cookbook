import typer
import requests
import time

DOMAIN = 'dev-aoojpnwcqsr11uc1.uk.auth0.com'
CLIENT_ID = 'TJ0Qv9mrw5eqFM9GBVSWIiazFKcbmV70'
CLIENT_SECRET = 'IOdSmVgj68JGGuQt0H0FLV-jqNvUKbYTqPzotOFaIh0-QdVihOCIll6yHHgh0p4T'
GRANT_TYPE = 'password'

app = typer.Typer()


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

    url = f"https://{DOMAIN}/oauth/token"
    response = requests.post(url, data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


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

    url = f"https://{DOMAIN}/oauth/token"
    response = requests.post(url, data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


@app.command()
def oidc_logout():

    payload = {
        'client_id': CLIENT_ID
    }

    url = f"https://{DOMAIN}/oidc/logout"
    response = requests.post(url, data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        print("success")
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


@app.command()
def oauth_device_code():

    payload = {
        'client_id': CLIENT_ID,
        'scope': 'openid'
    }

    url = f"https://{DOMAIN}/oauth/device/code"
    response = requests.post(url, data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


@app.command()
def oauth_token_loop(device_code: str, interval: int):

    token_payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code,
        'client_id': CLIENT_ID
    }

    authenticated = False
    while not authenticated:
        url = f"https://{DOMAIN}/oauth/token"
        token_response = requests.post(url, data=token_payload)

        token_json = token_response.json()
        print(token_json)

        if token_response.status_code == 200:
            authenticated = True
        elif token_json['error'] not in ('authorization_pending', 'slow_down'):
            raise typer.Exit(code=1)
        else:
            time.sleep(interval)


@app.command()
def oauth_token(device_code: str, interval: int):

    payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code,
        'client_id': CLIENT_ID
    }

    url = f"https://{DOMAIN}/oauth/token"
    response = requests.post(url, data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


if __name__ == "__main__":
    app()
