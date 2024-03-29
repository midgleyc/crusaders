#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import sys
import tempfile

from copy import deepcopy

from PIL import Image
from swf.movie import SWF
from swf.export import SVGExporter
from swf.tag import *

def convert(args):
    infile = getattr(args, 'input-file')
    swf = SWF(infile)

    if args.output_file:
        outfile = args.output_file
    else:
        outfile = os.path.basename(infile.name)

    mo = re.compile(r'(.*)[.](swf|png|svg)', re.I).match(outfile)
    if mo:
        outfile = mo.group(1)

    width = None
    height = None

    original_tags = deepcopy(swf.tags)
    original_frames = list(args.frames)

    max_frame_number = 0
    for tag in original_tags:
        if isinstance(tag, TagShowFrame):
            max_frame_number += 1

    frame_number_width = len(str(max_frame_number))

    if args.svg:
        tempdir = None
    else:
        tempdir = tempfile.mkdtemp()

    frame = 0
    frame_range = []
    done = False
    i = 0
    tags = []
    while not done:
        while i < len(original_tags):
            tag = original_tags[i]
            if isinstance(tag, TagPlaceObject2):
                matched = False
                # try to find a previous PlaceObject tag with the same characterId or depth, then
                # overwrite its matrix and/or colorTransform with this tag's to update its
                # properties
                for j in range(len(tags)):
                    tt = tags[j]
                    if isinstance(tt, TagPlaceObject) and \
                        ((tag.characterId != -1 and tt.characterId == tag.characterId) or \
                         (tag.characterId == -1 and tt.depth == tag.depth)):
                        if tag.hasMatrix:
                            tt.matrix = tag.matrix
                        if tag.hasColorTransform:
                            tt.colorTransform = tag.colorTransform
                        matched = True
                        break

                if not matched:
                    tags.append(tag)

                i += 1

            elif isinstance(tag, TagShowFrame):
                tags.append(tag)
                frame_range = [frame]
                i += 1
                frame += 1

                # consecutive ShowFrame tags mean no change in the frame, so don't export them all
                # repeatedly
                while i < len(original_tags) - 1 and \
                      isinstance(original_tags[i], TagShowFrame) and \
                      isinstance(original_tags[i + 1], TagShowFrame):
                    i += 1
                    frame += 1

                frame_range.append(frame)
                break

            elif isinstance(tag, TagEnd):
                done = True
                break

            else:
                tags.append(tag)
                i += 1

        if done:
            break

        if args.frames == "all":
            # export every frame, so just continue
            pass
        elif frame_range[0] <= args.frames[0] < frame_range[1]:
            # pop all frames covered by the current frame range
            while args.frames and frame_range[0] <= args.frames[0] < frame_range[1]:
                args.frames.pop(0)
            # and continue to export the frame
        else:
            # not a frame we want
            continue

        swf.tags = tags

        svg_exporter = SVGExporter()
        svgdata = swf.export(svg_exporter, force_stroke=not args.no_force_stroke)

        if args.frames != "all" and max_frame_number == 1:
            outfilename = outfile
        elif frame_range[0] < frame_range[1] - 1:
            format = '.%%0%dd-%%0%dd' % (frame_number_width, frame_number_width)
            outfilename = outfile + format % (frame_range[0], frame_range[1] - 1)
        else:
            format = '.%%0%dd' % frame_number_width
            outfilename = outfile + format % (frame - 1)

        print("exporting %s..." % outfilename)
        cursvgfile = outfilename + '.svg'
        if not args.svg:
            cursvgfile = os.path.join(tempdir, os.path.basename(cursvgfile))

        open(cursvgfile, 'wb').write(svgdata.read())

        if not args.frames:
            break

    if tempdir:
        shutil.rmtree(tempdir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert SWF to SVG and PNG")
    parser.add_argument('-o', '--output-file',
        help="output filename, .png or .svg and if needed a frame number is added automatically, "
             "default: input file name, current directory")
    parser.add_argument('--svg', action="store_true", default=True, help="export SVG file")
    parser.add_argument('-w', '--width', type=int,
        help="width of the PNG, no effect for the SVG export, has precedence over --scale")
    parser.add_argument('-t', '--height', type=int,
        help="height of the PNG, no effect on the SVG export, has precedence over --scale")
    parser.add_argument('-s', '--scale', type=float,
        help="scale of the PNG, no effect on the SVG export")
    parser.add_argument('-f', '--frames', default="0",
        help="frames to export, either 'all', comma separated frame numbers, "
             "or a range (e.g. 4,3-10,18,20-25), default: 0 (first frame only)")
    parser.add_argument('--super-scale', type=float,
        help="super scale factor, render to a larger image and then resize it down (slower)")
    parser.add_argument('-n', '--no-force-stroke', action="store_true",
        help="don't force shape strokes, default is to force them")
    parser.add_argument('input-file', type=argparse.FileType('rb'), help="input SWF file")
    args = parser.parse_args()

    if args.frames:
        args.frames = args.frames.lower()
    else:
        args.frames = "0"

    if args.frames != "all":
        chunks = args.frames.split(',')
        args.frames = []
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk.isdigit():
                args.frames.append(int(chunk))
                continue

            mo = re.match(r'^([0-9]+)-([0-9]+)', chunk)
            if mo:
                start = int(mo.group(1))
                end = int(mo.group(2))
                if start > end:
                    raise Exception("frame range start must be lower than or equal to end")
                for i in range(start, end + 1):
                    args.frames.append(i)
                continue

            raise Exception("couldn't understand frame number or range: '%s'" % chunk)

        args.frames = list(sorted(set(args.frames)))

    convert(args)
