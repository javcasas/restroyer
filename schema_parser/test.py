import unittest
import parser

class TestParser(unittest.TestCase):
    def check_result(self, text, result):
        self.assertEqual(parser.parse(text), result)

    def test_empty_file(self):
        self.check_result("", {})

    def test_ignore_comments(self):
        self.check_result("-- sdafdf", {})

    def test_empty_schema(self):
        self.check_result("create schema api;", {"api": {}})

    def test_empty_schema2(self):
        self.check_result("create schema api2;", {"api2": {}})

    def test_empty_schema3(self):
        self.check_result(
            "create schema api2; create schema api3;",
            {"api2": {}, "api3": {}}
        )

    def test_schema_with_table(self):
        self.check_result(
            """
            create schema api;
            create table api.todos (
                id integer not null,
                done boolean default false not null,
                task text not null,
                due timestamp with time zone
            );
            """,
            {"api": {
                "todos": {
                    "id": ["INTEGER"],
                    "done": ["BOOLEAN"],
                    "task": ["TEXT"],
                    "due": ["TIMESTAMP", "NULL"]
                    }
                }
            }
        )
class TestParseTable(unittest.TestCase):
    def test_parse_1(self):
        self.assertEqual(parser.parse_table("( id integer )"), {"id": ["INTEGER", "NULL"]})
    def test_parse_2(self):
        self.assertEqual(parser.parse_table("( id integer, done boolean )"), {"id": ["INTEGER", "NULL"], "done": ["BOOLEAN", "NULL"]})
    def test_parse_3(self):
        self.assertEqual(parser.parse_table("( id integer, done boolean not null )"), {"id": ["INTEGER", "NULL"], "done": ["BOOLEAN"]})

if __name__ == '__main__':
    unittest.main()
