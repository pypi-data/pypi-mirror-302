#tests for helper functions
# tests/test_helpers.py

import unittest
from my_asm_lib.helpers import format_registers, format_memory

class TestHelpers(unittest.TestCase):
    def test_format_registers(self):
        registers = {'ax': 10, 'bx': 20}
        result = format_registers(registers)
        self.assertEqual(result, "AX: 10\nBX: 20")

    def test_format_memory(self):
        memory = [0, 1, 2, 3, 4]
        result = format_memory(memory, 0, 3)
        self.assertEqual(result, "Address 0: 0\nAddress 1: 1\nAddress 2: 2")

if __name__ == '__main__':
    unittest.main()

