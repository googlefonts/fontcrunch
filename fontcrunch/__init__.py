from __future__ import print_function
from fontTools import ttLib

from .fontcrunch import optimize_glyph, plot_glyph

def optimize(fn, newfn, plot=None, penalty=None, quiet=False):
    f = ttLib.TTFont(fn)
    glyf = f['glyf']

    pdf = None
    if plot is not None:
        from reportlab.pdfgen import canvas
        pdf = canvas.Canvas(plot)

    for name in glyf.keys():
        g = glyf[name]
        plot_glyph(f, name, pdf, True)

        if not quiet:
            print('optimizing', name)
        optimize_glyph(g, penalty)

        plot_glyph(f, name, pdf, False)

    f.save(newfn)
    if plot is not None:
        pdf.save()
