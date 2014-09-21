import sys

from fontcrunch import optimize


def main(argv):
    if len(argv) >= 2:
        optimize(sys.argv[1], sys.argv[2] if len(argv) >= 3 else sys.argv[1], sys.argv[3] if len(argv) >= 4 else None)


if __name__ == '__main__':
    main(sys.argv)
