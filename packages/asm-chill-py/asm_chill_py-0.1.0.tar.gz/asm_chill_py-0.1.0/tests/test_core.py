#Tests for the CPU class and run_assembly functions
# tests/test_core.py

import unittest
from my_asm_lib.core import CPU

class TestCPU(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()

    def test_mov(self):
        self.cpu.mov('ax', 10)
        self.assertEqual(self.cpu.registers['ax'], 10)

    def test_add(self):
        self.cpu.mov('bx', 5)
        self.cpu.add('bx', 3)
        self.assertEqual(self.cpu.registers['bx'], 8)

    def test_sub(self):
        self.cpu.mov('cx', 15)
        self.cpu.sub('cx', 5)
        self.assertEqual(self.cpu.registers['cx'], 10)

if __name__ == '__main__':
    unittest.main()

