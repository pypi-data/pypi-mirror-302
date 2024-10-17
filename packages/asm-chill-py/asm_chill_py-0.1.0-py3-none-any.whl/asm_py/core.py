import subprocess
import os

class CPU:
    def __init__(self):
        # Initialize general-purpose registers
        self.registers = {
            'ax': 0,
            'bx': 0,
            'cx': 0,
            'dx': 0
        }
        self.memory = [0] * 1024 # 1kb memory 

    def mov(self, register, value):
        if register in self.registers:
            self.registers[register] = value
        else:
            raise ValueError(f"Register {register} not recognized.")

    def add(self, register, value):
        """
        ADD instruction which add a value to a register
        """
        if register in self.registers:
            self.registers[register] += value
        else:
            raise ValueError(f"Register {register} not recognized.")
    
    def sub(self, register, value):
        """
        SUB instruction which subtracts value from register
        """
        if register in self.registers:
            self.registers[register] -= value
        else:
            raise ValueError(f"Register {register} not recognized.")
    
    def print_registers(self):
        """
        current state of register
        """
        print("CPU Registers:")
        for reg, val in self.registers.items():
            print(f"{reg.upper()}: {val}")

    def load_to_memory(self, address, value):
        """
        load value of specific memory state
        """
        if 0 <= address < len(self.memory):
            self.memory[address] = value
        else:
            raise ValueError(f"Memory address {address} out of bounds.")

    def print_memory(self, start=0, end=10):
        """
        segment of memory start to end
        """
        print("Memory Dump:")
        for i in range(start, min(end, len(self.memory))):
            print(f"Address {i}: {self.memory[i]}")


def run_assembly(assembly_code: str, filename='temp.asm'):
    """
    Compiles and runs assembly code using NASM and the system's linker (ld).
    """
    try:
        with open(filename, 'w') as f:
            f.write(assembly_code)
        print(f"Assembly code saved to {filename}.")

        subprocess.run(['nasm', '-f', 'elf64', filename], check=True)
        subprocess.run(['ld', '-o', 'output', 'temp.o'], check=True)

        result = subprocess.run(['./output'], capture_output=True, text=True)
        print("Execution result:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        for file in [filename, 'temp.o', 'output']:
            if os.path.exists(file):
                os.remove(file)

