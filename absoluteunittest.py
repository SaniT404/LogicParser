import unittest
from logiparse import Logiparse

class TestLogiparseMethods(unittest.TestCase):

    def test_validateformat(self):
        logic = Logiparse()

        res, err = logic.validateFormat("A + B")
        self.assertEqual(res, True)

        res, err = logic.validateFormat("A * B")
        self.assertEqual(res, True)

        res, err = logic.validateFormat("A + (B * C)")
        self.assertEqual(res, True)

        res, err = logic.validateFormat("A + (B * C + (Dooby * Dilly))")
        self.assertEqual(res, True)

        res, err = logic.validateFormat("A' + (B * C' + (Dooby * Dilly'))")
        self.assertEqual(res, True)

if __name__ == '__main__':
    unittest.main()
