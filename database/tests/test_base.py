import migrate
import unittest

class TestBase(unittest.TestCase):

    def setUp(self):
        try:
            migrate.runMigrations()
        except:
            self.tearDown()
            raise
        self.cursor = migrate.getPostgres()

    def tearDown(self):
        migrate.resetDb()
