import sys

from fontcrunch import generate, repack


def main(argv):
    if argv[1] == 'gen':
        generate(sys.argv[2])
    elif argv[1] == 'pack':
        repack(sys.argv[2], sys.argv[3] if len(argv) >= 3 else None)


if __name__ == '__main__':
    main(sys.argv)
