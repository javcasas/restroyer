import jwt
import base64
import unittest

class TestJWT(unittest.TestCase):

    def test_authed_patch_todos(self):
        secret = "3jPpMqZaBRpVOJsME54DtzLGclCAw7d0"
        message = {"role": "todo_user"}
        token = jwt.encode(message, secret, algorithm='HS256')

        #token = jwt.encode(message, secret, algorithm='HS256')
        correct_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidG9kb191c2VyIn0._mlOzX51SFWT5PZvWHjFJJ7nR4Ch7E8tGYK5mpOn2so"
        [a, b, sign] = str(token).split(".")
        [ga, gb, gsign] = str(correct_token).split(".")
        print(token)
        print(base64.standard_b64decode(a+ "===="))
        print(base64.standard_b64decode(b+ "="))
        self.assertEqual(a, ga)
        self.assertEqual(b, gb)
        self.assertEqual(sign, gsign)
