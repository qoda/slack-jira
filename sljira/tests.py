import os
import unittest

from sljira import db


class DBTestCase(unittest.TestCase):
    def setUp(self):
        self.key = "test_key"
        self.value = "test_value"
        self.keyvalstore = db.KeyValStore(db_name="test.db")

    def test_keyvalstore(self):
        self.keyvalstore.set(self.key, self.value)
        value = self.keyvalstore.get(self.key)

        # Ensure the entry is save and can be accessed again
        self.assertEqual(self.value, value)

        # Ensure the no exception is raised if a value can not be found and
        # none is returned
        self.assertEqual(self.keyvalstore.get("fake_key"), None)

    def tearDown(self):
        os.remove(os.path.join(os.path.dirname(__file__), "../", "test.db"))


if __name__ == '__main__':
    unittest.main()
