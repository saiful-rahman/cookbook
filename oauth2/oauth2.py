import requests
# import time
import json


class OAuth2:

    __domain = None
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
        self.__device_code_url = f"https://{self.__domain}/oauth/device/code"
        self.__token_url = f"https://{self.__domain}/oauth/token"
        self.__authorize_url = f"https://{self.__domain}/authorize"
        self.__logout_url = f"https://{self.__domain}/oidc/logout"
        self.__jwks_url = f"https://{self.__domain}/.well-known/jwks.json"

    def print(self):
        print(f"domain: {self.__domain}")
        print(f"device_code_url: {self.__device_code_url}")
        print(f"token_url: {self.__token_url}")
        print(f"authorize_url: {self.__authorize_url}")
        print(f"jwks_url: {self.__jwks_url}")
        print(f"logout_url: {self.__logout_url}")
        print(f"client_id: {self.__client_id}")
        print(f"client_secret: {self.__client_secret}")

    def get_access_token(self, audience: str, username: str, password: str):

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

# from auth0 import Auth0Error
# from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
#
#
# def load_config(config_file: str):
#     config_file = open(config_file, 'r')
#     cfg = json.load(config_file)
#     return cfg
#
#
# # python3 auth0/auth0_cli.py get-access-token 'https://test/api' 'a@b.com' 'password'
# def get_access_token(cfg: dict, audience: str, username: str, password: str):
#
#     payload = {
#         'client_id': cfg['client_id'],
#         'client_secret': cfg['client_secret'],
#         'username': username,
#         'password': password,
#         'audience': audience,
#         'grant_type': 'password'
#     }
#
#     response = requests.post(cfg['token_url'], data=payload)
#     print(f"status_code:{response.status_code}")
#
#     if response.status_code == 200:
#         response_json = response.json()
#         print(response_json)
#     else:
#         print(f"failed: status-code:{response.status_code}, error-text:{response.text}")
#
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
# # $ python auth0/auth0_cli.py oauth-device-code
# def oauth_device_code(cfg: dict):
#
#     payload = {
#         'client_id': cfg['client_id'],
#         'scope': 'openid'
#     }
#
#     response = requests.post(cfg['device_code_url'], data=payload)
#     print(f"status_code:{response.status_code}")
#
#     if response.status_code == 200:
#         response_json = response.json()
#         print(response_json)
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
#
#
# # $ python auth0/auth0_cli.py oauth-token x472JUkihP_Zft3qrPPNo95I
# def oauth_token(cfg: dict, device_code: str):
#
#     payload = {
#         'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
#         'device_code': device_code,
#         'client_id': cfg['client_id']
#     }
#
#     response = requests.post(cfg['token_url'], data=payload)
#     print(f"status_code:{response.status_code}")
#
#     if response.status_code == 200:
#         response_json = response.json()
#         print(response_json)
#     else:
#         print(f"failed: status-code:{response.status_code}, error-text:{response.text}")
#
#
# def verify_token(cfg: dict, id_token: str):
#
#     signature_verifier = AsymmetricSignatureVerifier(cfg['jwks_url'])
#     issuer = cfg['issuer'] + '/'
#
#     try:
#         token_verifier = TokenVerifier(signature_verifier=signature_verifier, issuer=issuer, audience=cfg['client_id'])
#         token_info = token_verifier.verify(id_token)
#         print(token_info)
#     except Auth0Error as e:
#         # Handle Auth0 errors
#         print(f"Auth0Error: {e}")
#     except Exception as e:
#         # Handle other unexpected errors
#         print(f"Unexpected error: {e}")
