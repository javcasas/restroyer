import test_base

class TestMigrationsRunProperly(test_base.TestBase):

    def test_all_todos_exist(self):
        self.cursor.execute("select * from api.todos;")
        self.assertEqual(self.cursor.fetchall(), [(1, False, 'finish tutorial 0', None), (2, False, 'pat self on back', None)])

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
