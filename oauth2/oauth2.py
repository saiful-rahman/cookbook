import requests
# import time
import json

from auth0 import Auth0Error
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier


class OAuth2:

    __domain = None
    __issuer = None
    __device_code_url = None
    __token_url = None
    __authorize_url = None
    __logout_url = None
    __jwks_url = None
    __client_id = None
    __client_secret = None

    def __int__(self):
        pass

    def load_config(self, json_config: str):
        fh = open(json_config, 'r')
        cfg = json.load(fh)
        self.set_domain(cfg['domain'])
        self.set_client_id(cfg['client_id'])
        self.set_client_secret(cfg['client_secret'])

    #     self.set_domain(domain)
    #     self.__create_api_urls()

    def set_domain(self, domain: str):
        self.__domain = domain
        self.__create_api_urls()

    def set_issuer(self, issuer: str):
        self.__issuer = issuer

    def set_device_code_url(self, device_code_url: str):
        self.__device_code_url = device_code_url

    def set_token_url(self, token_url: str):
        self.__token_url = token_url

    def set_authorize_url(self, authorize_url: str):
        self.__authorize_url = authorize_url

    def set_logout_url(self, logout_url: str):
        self.__logout_url = logout_url

    def set_jwks_url(self, jwks_url: str):
        self.__jwks_url = jwks_url

    def set_client_id(self, client_id: str):
        self.__client_id = client_id

    def set_client_secret(self, client_secret: str):
        self.__client_secret = client_secret

    def get_domain(self):
        return self.__domain

    def get_issuer(self):
        return self.__issuer

    def get_device_code_url(self):
        return self.__device_code_url

    def get_token_url(self):
        return self.__token_url

    def get_authorize_url(self):
        return self.__authorize_url

    def get_logout_url(self):
        return self.__logout_url

    def get_jwks_url(self):
        return self.__jwks_url

    def get_client_id(self):
        return self.__client_id

    def get_client_secret(self):
        return self.__client_secret

    def __create_api_urls(self):
        self.__issuer = f"https://{self.get_domain()}/"
        self.__device_code_url = f"https://{self.get_domain()}/oauth/device/code"
        self.__token_url = f"https://{self.get_domain()}/oauth/token"
        self.__authorize_url = f"https://{self.get_domain()}/authorize"
        self.__logout_url = f"https://{self.get_domain()}/oidc/logout"
        self.__jwks_url = f"https://{self.get_domain()}/.well-known/jwks.json"

    def print(self):
        print(f"domain: {self.get_domain()}")
        print(f"issuer: {self.get_issuer()}")
        print(f"device_code_url: {self.get_device_code_url()}")
        print(f"token_url: {self.get_token_url()}")
        print(f"authorize_url: {self.get_authorize_url()}")
        print(f"jwks_url: {self.get_jwks_url()}")
        print(f"logout_url: {self.get_logout_url()}")
        print(f"client_id: {self.get_client_id()}")
        print(f"client_secret: {self.get_client_secret()}")

    def access_token(self, audience: str, username: str, password: str):

        data = {
            'client_id': self.get_client_id(),
            'client_secret': self.get_client_secret(),
            'username': username,
            'password': password,
            'audience': audience,
            'grant_type': 'password'
        }

        response = requests.post(self.get_token_url(), data=data)
        status_code = response.status_code
        response_json = response.json()
        return status_code, response_json

    # $ python auth0/auth0_cli.py oauth-device-code
    def oauth_device_code(self):

        payload = {
            'client_id': self.get_client_id(),
            'scope': 'openid'
        }

        response = requests.post(self.get_device_code_url(), data=payload)
        status_code = response.status_code
        response_json = response.json()
        return status_code, response_json

    def oauth_token(self, device_code: str):

        payload = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code,
            'client_id': self.get_client_id()
        }

        response = requests.post(self.get_token_url(), data=payload)
        status_code = response.status_code
        response_json = response.json()
        return status_code, response_json

    def verify_token(self, id_token: str):

        signature_verifier = AsymmetricSignatureVerifier(self.get_jwks_url())
        issuer = self.get_issuer()

        try:
            token_verifier = TokenVerifier(signature_verifier=signature_verifier, issuer=issuer, audience=self.get_client_id())
            token_info = token_verifier.verify(id_token)
            return token_info
        except Exception as e:
            raise e

    def oidc_logout(self):

        payload = {
            'client_id': self.get_client_id(),
        }

        response = requests.post(self.get_logout_url(), data=payload)
        status_code = response.status_code
        return status_code

# from auth0 import Auth0Error
# from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
#
# # $ python auth0/auth0_cli.py oidc-logout
# def oidc_logout(cfg: dict):
#
#     payload = {
#         'client_id': cfg['client_id'],
#     }
#
#     response = requests.post(cfg['logout_url'], data=payload)
#     print(f"status_code:{response.status_code}")
#
#     if response.status_code == 200:
#         print("success")
#     else:
#         print(f"failed: status-code:{response.status_code}, error-text:{response.text}")
#
#
# def oauth_token_loop(cfg: dict, device_code: str, interval: int):
#
#     token_payload = {
#         'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
#         'device_code': device_code,
#         'client_id': cfg['client_id']
#     }
#
#     authenticated = False
#     while not authenticated:
#         token_response = requests.post(cfg['token_url'], data=token_payload)
#
#         token_json = token_response.json()
#         print(token_json)
#
#         if token_response.status_code == 200:
#             authenticated = True
#         elif token_json['error'] not in ('authorization_pending', 'slow_down'):
#             raise typer.Exit(code=1)
#         else:
#             time.sleep(interval)
