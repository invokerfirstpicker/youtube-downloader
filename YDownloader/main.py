import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import main as cli_main

if __name__ == "__main__":
    cli_main()