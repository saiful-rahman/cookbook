import unittest
from oauth2 import OAuth2
import configparser


class MyTestCase(unittest.TestCase):

    def test_domain_urls(self):
        oauth2 = OAuth2()
        oauth2.set_domain('saif')
        self.assertIsNotNone(oauth2.get_domain())
        self.assertIsNotNone(oauth2.get_device_code_url())
        self.assertIsNotNone(oauth2.get_token_url())
        self.assertIsNotNone(oauth2.get_authorize_url())
        self.assertIsNotNone(oauth2.get_jwks_url())
        self.assertIsNotNone(oauth2.get_logout_url())
        oauth2.print()

    def test_load_config(self):
        config = configparser.ConfigParser()
        config.read('../config/credentials.ini')
        oauth2 = OAuth2()
        oauth2.load_config(json_config='../config/mini-native-app.json')

        self.assertIsNotNone(oauth2.get_client_id())
        self.assertIsNotNone(oauth2.get_client_secret())
        oauth2.print()
        response = oauth2.access_token('https://test/api', config['credentials']['username'], config['credentials']['password'])
        print(response)

    def test_device_code(self):
        oauth2 = OAuth2()
        oauth2.load_config(json_config='../config/mini-native-app.json')
        # oauth2.print()
        response = oauth2.oauth_device_code()
        print(response)

    def test_oauth_token(self):
        oauth2 = OAuth2()
        oauth2.load_config(json_config='../config/mini-native-app.json')
        # oauth2.print()
        response = oauth2.oauth_token('EdUbAOSdZht2lEbDPfjn3nnf')
        print(response)

    def test_verify_token(self):
        oauth2 = OAuth2()
        oauth2.load_config(json_config='../config/mini-native-app.json')
        # oauth2.print()
        try:
            response = oauth2.verify_token('eyJhbGciOiJS')
            print(response)
        except Exception as e:
            print(e)

    def test_oidc_logout(self):
        oauth2 = OAuth2()
        oauth2.load_config(json_config='../config/mini-native-app.json')
        # oauth2.print()
        status_code = oauth2.oidc_logout()
        print(status_code)


if __name__ == '__main__':
    unittest.main()
