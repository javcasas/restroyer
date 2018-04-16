import test_base
import requests
import jwt
import functools

def NetTester(secret=None, claims=None):
    headers = {}
    if secret and claims:
        token = jwt.encode(claims, secret, algorithm='HS256').decode("utf-8")
        headers["Authorization"] = "Bearer " + token
    class NT: pass
    x = NT()
    for method in ["get", "post", "patch", "delete"]:
        x.__setattr__(method, functools.partial(requests.__getattribute__(method), headers=headers))
    return x

class TestMigrationsRunProperly(test_base.TestBase):

    def setUp(self):
        super(TestMigrationsRunProperly, self).setUp()
        self.noAuthNetTester = NetTester()
        self.authedNetTester = NetTester(
                            secret="3jPpMqZaBRpVOJsME54DtzLGclCAw7d0",
                            claims={"role": "todo_user"}
                        )

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
        req = self.noAuthNetTester.get("http://localhost:3000/todos")
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
        req = self.authedNetTester.patch("http://localhost:3000/todos", {"done": True})
        self.assertSuccessNoContent(req)

    def test_there_is_a_user_table(self):
        self.cursor.execute("select * from backend.users;")
        self.assertEqual(self.cursor.fetchall(),
            []
        )

    def test_the_user_table_contains_user_password_role(self):
        self.cursor.execute("insert into backend.users (uname, pw, role) values ('john','secret','todo_user');")
        self.cursor.execute("select * from backend.users;")
        self.assertEqual(self.cursor.fetchall(),
            [(1, "john", "secret", "todo_user")]
        )

    def test_authing(self):
        self.cursor.execute("""
                insert into backend.users (uname, pw, role)
                values ('john','secret','todo_user');""")
        v = self.noAuthNetTester.post("http://localhost:3000/rpc/login",
                {"username": "john", "password": "secret"})
        self.assertIn("token", v.json()[0])

    def test_no_authing(self):
        self.cursor.execute("""
                insert into backend.users (uname, pw, role)
                values ('john','secret','todo_user');""")
        v = self.noAuthNetTester.post("http://localhost:3000/rpc/login",
                {"username": "john", "password": "bad_password"})
        self.assertEqual(v.json(), [{"token": None}])
