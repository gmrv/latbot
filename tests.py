import unittest
from common.lastb_entry import LastbEntry
from common.utils import get_last_btmp_entry
from main import login_attempts_checker

class EntryTest(unittest.TestCase):

    @staticmethod
    def entry_compare(e1, e2, msg=None):
        if not e1.is_equal(e2):
            raise AssertionError("e1 not equal e2", str(e1), str(e2))

    def setUp(self):

        self.addTypeEqualityFunc(LastbEntry, self.entry_compare)

    def test_is_empty(self):
        e1 = LastbEntry(None, None, None)
        self.assertEqual(e1.is_empty(), True)  # add assertion here

    def test_to_string(self):
        e1 = LastbEntry("user", "1.1.1.1", 12345678)
        self.assertEqual(str(e1), '{"username": "user", "host": "1.1.1.1", "timestamp": "12345678"}')

    def test_is_equal_1(self):
        e1 = LastbEntry("user", "1.1.1.1", 12345678)
        e2 = LastbEntry("user", "1.1.1.1", 12345678)
        self.assertEqual(e1, e2, "1")

    def test_is_equal_2(self):
        e1 = LastbEntry("resu", "2.2.2.2", 87654321)
        e2 = LastbEntry("user", "1.1.1.1", 12345678)
        if e1.is_equal(e2):
            raise self.failureException("e1 equal e2", str(e1), str(e2))

        self.assertNotEqual(e1, e2, "2")

class UtilsTest(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(LastbEntry, EntryTest.entry_compare)

    def test_get_last_btmp_entry_1(self):
        e1 = LastbEntry("proxy", "", 1639782636)
        e2 = get_last_btmp_entry()
        self.assertEqual(e1, e2, None)

    def test_get_last_btmp_entry_2(self):
        e2 = get_last_btmp_entry()
        self.assertEqual(e2.is_empty(), False, "Entry is empty")

    def test_login_attempts_checker(self):
        result = login_attempts_checker(None)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()