# tests for parsing assembly instructions correctly.
# tests/test_parsers.py

import unittest
from my_asm_lib.parsers import parse_instruction, parse_program

class TestParsers(unittest.TestCase):
    def test_parse_instruction(self):
        instruction = 'MOV ax, 5'
        result = parse_instruction(instruction)
        self.assertEqual(result, ('MOV', 'AX', 5))

    def test_parse_program(self):
        program = """
        MOV ax, 5
        ADD bx, 10
        """
        result = parse_program(program)
        expected = [('MOV', 'AX', 5), ('ADD', 'BX', 10)]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

