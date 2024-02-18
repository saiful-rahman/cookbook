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
        # oauth2.print()

    def test_load_config(self):
        config = configparser.ConfigParser()
        config.read('../config/credentials.ini')
        oauth2 = OAuth2()
        oauth2.load_config(json_config='../config/mini-native-app.json')

        self.assertIsNotNone(oauth2.get_client_id())
        self.assertIsNotNone(oauth2.get_client_secret())
        # oauth2.print()
        # response = oauth2.get_access_token('https://test/api', config['credentials']['username'], config['credentials']['password'])
        # print(response)


if __name__ == '__main__':
    unittest.main()
