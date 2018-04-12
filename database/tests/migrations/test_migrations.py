import test_base
import requests
import jwt

class TestMigrationsRunProperly(test_base.TestBase):

    def setUp(self):
        super(TestMigrationsRunProperly, self).setUp()
        secret = "3jPpMqZaBRpVOJsME54DtzLGclCAw7d0"
        self.netTester = NetTester({"role": "todo_user"}, secret)

    def test_all_todos_exist(self):
        self.cursor.execute("select * from api.todos;")
        self.assertEqual(self.cursor.fetchall(),
            [(1, False, 'finish tutorial 0', None),
             (2, False, 'pat self on back', None)
            ]
        )

    def test_all_schemas_exists(self):
        self.cursor.execute("select schema_name from information_schema.schemata;")
        schemas = self.cursor.fetchall()
        self.assertIn(("api",), schemas)
        self.assertIn(("auth",), schemas)

    def test_all_roles_exists(self):
        self.cursor.execute("SELECT rolname FROM pg_catalog.pg_roles;")
        roles = self.cursor.fetchall()
        self.assertIn(("app_user",), roles)
        self.assertIn(("web_anon",), roles)
        self.assertIn(("todo_user",), roles)

    def assertSuccess(self, req):
        self.assertEqual(req.status_code, 200)

    def assertSuccessNoContent(self, req):
        self.assertEqual(req.status_code, 204)

    def assertSuccessWith(self, req, to_compare):
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.json(), to_compare)

    def assertNoAuth(self, req):
        self.assertEqual(req.status_code, 401)
        res = req.json()
        self.assertIsNone(res.get('hint'))
        self.assertIsNone(res.get('details'))
        self.assertTrue(res['message'].startswith('permission denied for relation'))
        self.assertEqual(res['code'], '42501')

    def test_get_todos(self):
        req = requests.get("http://localhost:3000/todos")
        self.assertSuccessWith(req, [
            {
                'done': False,
                'due': None,
                'id': 1,
                'task': 'finish tutorial 0'
            },
            {
                'done': False,
                'due': None,
                'id': 2,
                'task': 'pat self on back'
            }
        ])

    def test_fail_create_todos(self):
        req = requests.post("http://localhost:3000/todos",
            {
                'done': False,
                'due': None,
                'id': 2,
                'task': 'pat self on back'
            }
            )
        self.assertNoAuth(req)

    def test_fail_patch_todos(self):
        req = requests.patch("http://localhost:3000/todos", {"done": True})
        self.assertNoAuth(req)

    def test_fail_delete_todos(self):
        req = requests.delete("http://localhost:3000/todos")
        self.assertNoAuth(req)

    def test_authed_patch_todos(self):
        req = self.netTester.patch("http://localhost:3000/todos", {"done": True})
        self.assertSuccessNoContent(req)

class NetTester:
    def __init__(self, claims, secret):
        self.token = jwt.encode(claims, secret, algorithm='HS256').decode("utf-8")

    def get_headers(self):
        return {"Authorization": "Bearer " + self.token}

    def get(self, url):
        return requests.get(url, headers=self.get_headers())

    def post(self, url, data):
        return requests.post(url, data, headers=self.get_headers())

    def patch(self, url, data):
        return requests.patch(url, data, headers=self.get_headers())

    def delete(self, url):
        return requests.delete(url, headers=self.get_headers())
