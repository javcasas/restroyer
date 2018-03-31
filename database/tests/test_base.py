import migrate
import unittest

class TestBase(unittest.TestCase):

    def setUp(self):
        migrate.runMigrations()
        self.cursor = migrate.getPostgres()

    def tearDown(self):
        migrate.resetDb()
