# Add the parent directory of 'target_platforms' to the sys.path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gupy

gupy.main()