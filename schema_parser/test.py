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
        t =  """
            create schema api;
            create table api.todos (
                id integer not null,
                done boolean default false not null,
                task text not null,
                due timestamp with time zone
            );
            """
        print(parser.parse(t))
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
                    "due": ["TIMESTAMP+TZ", "NULL"]
                    }
                }
            }
        )
class TestParseTable(unittest.TestCase):
    def test_parse_1(self):
        self.assertEqual(
            parser.parse_table(
                ["(", "id", "INTEGER", ")"]),
            {"id": ["INTEGER", "NULL"]})
    def test_parse_2(self):
        self.assertEqual(
            parser.parse_table(
                ["(", "id", "INTEGER", ",", "done", "BOOLEAN", ")"]),
            {"id": ["INTEGER", "NULL"], "done": ["BOOLEAN", "NULL"]})
    def test_parse_3(self):
        self.assertEqual(
            parser.parse_table(
                ["(", "id", "INTEGER", ",", "done", "BOOLEAN", "NOT", "NULL", ")"]),
            {"id": ["INTEGER", "NULL"], "done": ["BOOLEAN"]})

class TestTokenizer(unittest.TestCase):
    def test_tokenize_comment(self):
        self.assertEqual(parser.tokenize("-- bdfsbdf"), ["COMMENT"])
    def test_tokenize_comment_2(self):
        self.assertEqual(parser.tokenize("-- bdfsbdf\n--bdfb"), ["COMMENT", "COMMENT"])
    def test_tokenize_1(self):
        self.assertEqual(parser.tokenize("create schema blah;"), ["CREATE", "SCHEMA", "blah", ";"])
    def test_tokenize_2(self):
        self.assertEqual(parser.tokenize("create schema blah; -- gdfg feg eggds \nCREATE Table pu;"), ["CREATE", "SCHEMA", "blah", ";", "COMMENT", "CREATE", "TABLE", "pu", ";"])
    def test_tokenize_3(self):
        self.assertEqual(parser.tokenize("create table blah.bleu;"), ["CREATE", "TABLE", "blah.bleu", ";"])

class TestContains(unittest.TestCase):
    def test_contains_1(self):
        self.assertTrue(parser.contains(["a", "b", "c", "d"], ["c", "d"]))
    def test_starts_1(self):
        self.assertTrue(parser.starts(["a", "b"], ["a", "b"]))

if __name__ == '__main__':
    unittest.main()
