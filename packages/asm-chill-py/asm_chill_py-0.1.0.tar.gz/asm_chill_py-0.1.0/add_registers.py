# we call ADD instruction
from asm_py.core import CPU

def add_registers():
    cpu = CPU()
    cpu.mov('ax', 10)  # Move 10 into AX
    cpu.add('ax', 5)   # Add 5 to AX
    cpu.print_registers()  # Print the register values

if __name__ == "__main__":
    add_registers()

