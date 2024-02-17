import typer
import requests
import time
import json

app = typer.Typer()

with open("config/native-app.json", "r") as config_file:
    oidc_config = json.load(config_file)


# python3 auth0/auth0.py get-access-token 'https://test/api' 'a@b.com' 'password'
@app.command()
def get_access_token(audience: str, username: str, password: str):

    payload = {
        'client_id': oidc_config['client_id'],
        'client_secret': oidc_config['client_secret'],
        'username': username,
        'password': password,
        'audience': audience,
        'grant_type': 'password'
    }

    response = requests.post(oidc_config['token_url'], data=payload)
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

    response = requests.post(oidc_config['token_url'], data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


@app.command()
def oidc_logout():

    payload = {
        'client_id': oidc_config['client_id'],
    }

    response = requests.post(oidc_config['logout_url'], data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        print("success")
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


@app.command()
def oauth_device_code():

    payload = {
        'client_id': oidc_config['client_id'],
        'scope': 'openid'
    }

    response = requests.post(oidc_config['device_code_url'], data=payload)
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
        'client_id': oidc_config['client_id']
    }

    authenticated = False
    while not authenticated:
        token_response = requests.post(oidc_config['token_url'], data=token_payload)

        token_json = token_response.json()
        print(token_json)

        if token_response.status_code == 200:
            authenticated = True
        elif token_json['error'] not in ('authorization_pending', 'slow_down'):
            raise typer.Exit(code=1)
        else:
            time.sleep(interval)


@app.command()
def oauth_token(device_code: str):

    payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code,
        'client_id': oidc_config['client_id']
    }

    response = requests.post(oidc_config['token_url'], data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


if __name__ == "__main__":
    app()
