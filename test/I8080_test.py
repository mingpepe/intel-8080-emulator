import unittest

from i8080 import I8080Chip

class TestI8080Chip(unittest.TestCase):
    def test_parity(self):
        self.assertTrue(I8080Chip.parity(0b110))
        self.assertTrue(I8080Chip.parity(0b1010))
        self.assertFalse(I8080Chip.parity(0b100))
        self.assertFalse(I8080Chip.parity(0b010))
        self.assertFalse(I8080Chip.parity(0b001))