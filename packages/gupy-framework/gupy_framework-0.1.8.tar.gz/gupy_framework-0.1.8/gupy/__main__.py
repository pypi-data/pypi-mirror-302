from gupy import gupy

def main():
    import sys
    import os
    # Add the parent directory of 'target_platforms' to the sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    gupy.main()

if __name__ == "__main__":
    main()