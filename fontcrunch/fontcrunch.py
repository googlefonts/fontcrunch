# coding: utf-8
# Copyright 2013 The Font Bakery Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See AUTHORS.txt for the list of Authors and LICENSE.txt for the License.
#
# Contributor: Raph Levien

from fontTools import ttLib
from fontTools.ttLib.tables import _g_l_y_f
import math
import md5
import quadopt

import os


def lerppt(t, p0, p1):
    return (p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]))


def glyph_to_bzs(g):
    bzs = []
    for i in range(g.numberOfContours):
        beg = 0 if i == 0 else g.endPtsOfContours[i - 1] + 1
        end = g.endPtsOfContours[i] + 1
        n = end - beg
        pts = g.coordinates[beg:end]
        flags = g.flags[beg:end]
        bz = []
        for j in range(n):
            x1, y1 = pts[(j+1) % n]
            if flags[j] and flags[(j+1) % n]:
                bz.append((pts[j], (x1, y1)))
            elif not flags[j]:
                if flags[j - 1]:
                    x0, y0 = pts[j - 1]
                else:
                    x0, y0 = lerppt(0.5, pts[j - 1], pts[j])
                if not flags[(j+1) % n]:
                    x1, y1 = lerppt(0.5, (x1, y1), pts[j])
                if tuple(pts[j]) == (x0, y0) or tuple(pts[j]) == (x1, y1):
                    # degenerate quad, treat as line
                    bz.append(((x0, y0), (x1, y1)))
                else:
                    bz.append(((x0, y0), pts[j], (x1, y1)))
        bzs.append(bz)
    return bzs

def segment_sp(sp):
    bks = set()

    # direction changes
    xsg = 0
    ysg = 0
    for i in range(2 * len(sp)):
        imod = i % len(sp)
        xsg1 = sp[imod][-1][0] - sp[imod][0][0]
        ysg1 = sp[imod][-1][1] - sp[imod][0][1]
        if xsg * xsg1 < 0 or ysg * ysg1 < 0:
            bks.add(imod)
            xsg = xsg1
            ysg = ysg1
        else:
            if xsg == 0: xsg = xsg1
            if ysg == 0: ysg = ysg1

    # angle breaks
    for i in range(len(sp)):
        dx0 = sp[i-1][-1][0] - sp[i-1][-2][0]
        dy0 = sp[i-1][-1][1] - sp[i-1][-2][1]
        dx1 = sp[i][1][0] - sp[i][0][0]
        dy1 = sp[i][1][1] - sp[i][0][1]
        bend = dx1 * dy0 - dx0 * dy1
        if (dx0 == 0 and dy0 == 0) or (dx1 == 0 and dy1 == 0):
            bks.add(i)
        else:
            bend = bend / (math.hypot(dx0, dy0) * math.hypot(dx1, dy1))
            # for small angles, bend is in units of radians
            if abs(bend) > 0.02:
                bks.add(i)

    return sorted(bks)

def seg_to_string(sp, bk0, bk1):
    if bk1 < bk0:
        bk1 += len(sp)
    res = []
    for i in range(bk0, bk1):
        bz = sp[i % len(sp)]
        if len(bz) == 2:
            # just represent lines as quads
            bz = (bz[0], lerppt(0.5, bz[0], bz[1]), bz[1])
        res.append(' '.join(['%g' % z for xy in bz for z in xy]) + '\n')
    return ''.join(res)

def optimize_glyph(glyph):
    bzs = glyph_to_bzs(glyph)
    newbzs = []
    for sp in bzs:
        bks = segment_sp(sp)
        newsp = []
        for i in range(len(bks)):
            bk0, bk1 = bks[i], bks[(i + 1) % len(bks)]
            if bk1 != (bk0 + 1) % len(sp) or len(sp[bk0]) != 2:
                segstr = seg_to_string(sp, bk0, bk1)
                optstr = quadopt.optimize(segstr)
                newsp.extend(read_bzs(optstr.strip()))
            else:
                newsp.append(sp[bk0])
        newbzs.append(newsp)
    bzs_to_glyph(newbzs, glyph)

def read_bzs(segstr):
    result = []
    for l in segstr.split("\n"):
        z = [float(z) for z in l.split()]
        bz = ((z[0], z[1]), (z[2], z[3]), (z[4], z[5]))
        if bz[1] == lerppt(0.5, bz[0], bz[2]):
            bz = (bz[0], bz[2])
        result.append(bz)
    return result

def pt_to_int(pt):
    # todo: should investigate non-int points
    return (int(round(pt[0])), int(round(pt[1])))

def bzs_to_glyph(bzs, glyph):
    coordinates = []
    flags = []
    endPtsOfContours = []
    for sp in bzs:
        for i in range(len(sp)):
            lastbz = sp[i - 1]
            bz = sp[i]
            if len(bz) != 3 or len(lastbz) != 3 or lerppt(0.5, lastbz[1], bz[1]) != bz[0]:
                coordinates.append(pt_to_int(bz[0]))
                flags.append(1)
            if len(bz) == 3:
                coordinates.append(pt_to_int(bz[1]))
                flags.append(0)
        endPtsOfContours.append(len(coordinates) - 1)
    glyph.coordinates = _g_l_y_f.GlyphCoordinates(coordinates)
    glyph.flags = flags
    glyph.endPtsOfContours = endPtsOfContours

def optimize(fn, newfn):
    f = ttLib.TTFont(fn)
    glyf = f['glyf']
    for name in glyf.keys():
        g = glyf[name]
        print 'optimizing', name
        optimize_glyph(g)

    f.save(newfn)
