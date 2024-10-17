#use for importing core modules into the package's namespace
#core functions import them here for convenience..

# Import core functionality from core.py
from .core import CPU , run_assembly

# Import instruction parsing functionality from parser.py
from .parsers import parse_instruction , parse_program
 
from .helpers import format_registers , format_memory


__version__= "1.0.0"

__all__ = ['CPU', 'run_assembly' , 'format_registers' , 'format_memory', 'parse_instruction' , 'parse_program']

# user can import 'CPU' , 'run_assembly' and 'parse_instruction'
# do 'from asm_lib import CPU , run_assembly , parse_instruction'

