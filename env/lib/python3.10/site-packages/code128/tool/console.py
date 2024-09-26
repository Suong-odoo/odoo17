#! /usr/bin/env python3

# Copyright (c) 2014-2015 Felix Knopf <felix.knopf@arcor.de>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License in the LICENSE.txt for more details.
#

import argparse
import os
from os.path import splitext
import code128

def main():
    """entry point for command line users"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Data, that should be encoded")
    parser.add_argument("output", help="File to store the barcode")
    parser.add_argument("-H", "--height", default=100, type=int,
                        help="height of generated picture in pixel, default: 100")
    parser.add_argument("-T", "--thickness", default=3, type=int,
                        help="width of a bar with weight=1 in pixel, default: 3")
    parser.add_argument("-q", "--no_quiet", action="store_false", default=True,
                        help="Do not include the quiet zone "
                                    "before and after the code in the picture")    
    args = parser.parse_args()

    ftype = splitext(args.output)[1]
    suptypes =  ".bmp .dib .gif .im .jpg .jpe .jpeg .pcx .png .pbm " \
                ".pgm .ppm .tif .tiff .xbm .xpm .svg".split()

    if ftype == ".svg":
        print("Barcode '%s' created" % args.data)
        with open(args.output, "w") as f:
            f.write(code128.svg(args.data, args.height,
                                args.thickness, args.no_quiet))
        print("Barcode successfully saved as", args.output)

    elif ftype in suptypes:
        img = code128.image(args.data, args.height,
                                args.thickness, args.no_quiet)
        print("Barcode '%s' created" % args.data)
        img.save(args.output)
        print("Barcode successfully saved as", args.output)

    else: print("Type '%s' is not supportet, use one of these: %s" % (ftype,
                " ".join(suptypes)) )
