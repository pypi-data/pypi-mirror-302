import argparse

from directory_tree import DisplayTree

parser = argparse.ArgumentParser(
    prog="dir-audit",
    description="Audit directory tree structure",
)

parser.add_argument("directory")
parser.add_argument("-c", "--contains")
parser.add_argument("-e", "--empty")

# Main Method
if __name__ == '__main__':
    args = parser.parse_args()

    DisplayTree(args.directory)
