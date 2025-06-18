#!/usr/bin/env python

"""
Voting Simulator CLI Runner
"""

import sys
import os

# Add the current directory to the path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import main


if __name__ == "__main__":
    main()
