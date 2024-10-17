#converting assembly instructions into executable operations.
# Mapping assembly mnemonics to operations in core.py
def parse_instruction(instruction: str):
    """
    Parses a single assembly-like instruction into its components.
    """
    instruction = instruction.strip().upper()
    parts = instruction.split()

    if len(parts) < 2:
        raise ValueError(f"Invalid instruction format: {instruction}")

    operation = parts[0]
    if operation == 'MOV' and len(parts) == 3:
        register = parts[1].replace(",", "")
        value = int(parts[2])
        return ('MOV', register, value)
    
    elif operation in ['ADD', 'SUB', 'MUL', 'DIV'] and len(parts) == 3:
        register = parts[1].replace(",", "")
        value = int(parts[2])
        return (operation, register, value)

    elif operation == 'INC' and len(parts) == 2:
        register = parts[1]
        return ('INC', register)

    elif operation == 'DEC' and len(parts) == 2:
        register = parts[1]
        return ('DEC', register)

    else:
        raise ValueError(f"Unsupported or improperly formatted instruction: {instruction}")


def parse_program(program: str):
    """
    Parses a multi-line string representing an assembly-like program into individual instructions.
    """
    lines = program.strip().splitlines()
    instructions = []
    
    for line in lines:
        if line.strip() and not line.startswith(";"):
            instruction = parse_instruction(line)
            instructions.append(instruction)

    return instructions

