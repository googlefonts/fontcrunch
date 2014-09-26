import argparse
from os import path
from fontcrunch import optimize


def main(args):
    infile = args.infile
    outfile = args.outfile
    plotfile = args.plotfile

    if not outfile:
        base, ext = path.splitext(infile)
        outfile = base + "-opt" + ext

    optimize(infile, outfile, plotfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Optimize TrueType font splines.")
    parser.add_argument("infile", metavar="FILE", help="name of input font to process")
    parser.add_argument("-o", dest="outfile", metavar="FILE", help="name of output font to write")
    parser.add_argument("-d", dest="plotfile", metavar="FILE", help="name of glyphs plot file")

    main(parser.parse_args())
