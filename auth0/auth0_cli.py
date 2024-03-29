import typer
import requests
import time
import json

from auth0 import Auth0Error
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier

cfg = dict()
app = typer.Typer()


def load_config(config_file: str):
    global cfg
    config_file = open(config_file, 'r')
    cfg = json.load(config_file)
    return cfg


# python3 auth0/auth0_cli.py get-access-token 'https://test/api' 'a@b.com' 'password'
@app.command()
def get_access_token(audience: str, username: str, password: str):

    payload = {
        'client_id': cfg['client_id'],
        'client_secret': cfg['client_secret'],
        'username': username,
        'password': password,
        'audience': audience,
        'grant_type': 'password'
    }

    response = requests.post(cfg['token_url'], data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


# $ python auth0/auth0_cli.py oidc-logout
@app.command()
def oidc_logout():

    payload = {
        'client_id': cfg['client_id'],
    }

    response = requests.post(cfg['logout_url'], data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        print("success")
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


# $ python auth0/auth0_cli.py oauth-device-code
@app.command()
def oauth_device_code():

    payload = {
        'client_id': cfg['client_id'],
        'scope': 'openid'
    }

    response = requests.post(cfg['device_code_url'], data=payload)
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
        'client_id': cfg['client_id']
    }

    authenticated = False
    while not authenticated:
        token_response = requests.post(cfg['token_url'], data=token_payload)

        token_json = token_response.json()
        print(token_json)

        if token_response.status_code == 200:
            authenticated = True
        elif token_json['error'] not in ('authorization_pending', 'slow_down'):
            raise typer.Exit(code=1)
        else:
            time.sleep(interval)


# $ python auth0/auth0_cli.py oauth-token x472JUkihP_Zft3qrPPNo95I
@app.command()
def oauth_token(device_code: str):

    payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code,
        'client_id': cfg['client_id']
    }

    response = requests.post(cfg['token_url'], data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


@app.command()
def verify_token(id_token: str):
    signature_verifier = AsymmetricSignatureVerifier(cfg['jwks_url'])
    issuer = cfg['issuer'] + '/'

    try:
        token_verifier = TokenVerifier(signature_verifier=signature_verifier, issuer=issuer, audience=cfg['client_id'])
        token_info = token_verifier.verify(id_token)
        print(token_info)
    except Auth0Error as e:
        # Handle Auth0 errors
        print(f"Auth0Error: {e}")
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    load_config("./config/native-app.json")
    app()
