import unittest
from logiparse import Logiparse

class TestLogiparseMethods(unittest.TestCase):

    def test_validateformat(self):
        logic = Logiparse()
        # Test OR
        res, err = logic.validateFormat("A + B")
        self.assertEqual(res, True)
        # Test AND
        res, err = logic.validateFormat("A * B")
        self.assertEqual(res, True)
        # Test parenthesis
        res, err = logic.validateFormat("A + (B * C)")
        self.assertEqual(res, True)
        # Test multiple operators, multicharacter variables, and multiple parenthesis
        res, err = logic.validateFormat("A + (B * C + (Dooby * Dilly))")
        self.assertEqual(res, True)
        # Test negation - beginning, middle, and end of equation with and without parenthesis
        res, err = logic.validateFormat("A' + (B * C' + (Dooby * Dilly')')")
        self.assertEqual(res, True)

if __name__ == '__main__':
    unittest.main()
