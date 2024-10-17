# helper functions for memory mangement or formatting register output.
# Utility for converting values between binary , hex and decimal.
# fuctions to validate input assembly code or sanitize registers names. 
# helper functions for formatting , validation or small utilities to enhance the library's functionality.
def format_registers(registers):
    """
    Formats the register values for display.
    """
    formatted = []
    for reg, val in registers.items():
        formatted.append(f"{reg.upper()}: {val}")
    return "\n".join(formatted)


def format_memory(memory, start=0, end=10):
    """
    Formats the memory for display.
    """
    formatted = []
    for i in range(start, min(end, len(memory))):
        formatted.append(f"Address {i}: {memory[i]}")
    return "\n".join(formatted)

