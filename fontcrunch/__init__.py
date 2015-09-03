from __future__ import print_function
from fontTools import ttLib
from multiprocessing import Pool

from .fontcrunch import optimize_glyph, plot_glyph

def _optimize(args):
    font, name, pdf, penalty, quiet = args
    if not quiet:
        print('optimizing', name)

    glyph = font['glyf'][name]
    plot_glyph(font, name, pdf, True)
    optimize_glyph(glyph, penalty)
    plot_glyph(font, name, pdf, False)
    if not quiet:
        print('done optimizing', name)
    return (name, glyph)

def _get_args(names, font, pdf, penalty, quiet):
    for name in names:
        yield font, name, pdf, penalty, quiet

def optimize(fn, newfn, plot=None, penalty=None, quiet=False, jobs=None):
    font = ttLib.TTFont(fn)
    glyf = font['glyf']

    pdf = None
    if plot is not None:
        from reportlab.pdfgen import canvas
        pdf = canvas.Canvas(plot)

    glyphs = []
    if jobs:
        pool = Pool(jobs)
        glyphs = pool.map(_optimize, _get_args(glyf.keys(), font, pdf, penalty, quiet))
        pool.close()
    else:
        glyphs = map(_optimize, _get_args(glyf.keys(), font, pdf, penalty, quiet))

    for name, glyph in glyphs:
        font['glyf'][name] = glyph

    font.save(newfn)
    if plot is not None:
        pdf.save()
