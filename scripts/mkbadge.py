# Copyright (C) 2016  Niklas Rosenstein
# All rights reserved.
#
# Create: 2016/02/19
# Last Modified: 2016/02/19
#
# Dirty script to generate a badge with a left- and right-side text.
# The font family and size and whether a red or green badge should
# be generated can be controlled via the command-line.
#
# Requires pyCairo.

import argparse
import cairo

COLOR_LEFT = (0.2, 0.2, 0.2)
COLOR_RIGHT_GOOD = (0.29, 0.79, 0.17)
COLOR_RIGHT_BAD  = (1.00, 0.39, 0.37)

rint = lambda x: int(round(x))


def main(argv=None, prog=None):
  parser = argparse.ArgumentParser(prog=prog)
  parser.add_argument('outfile')
  parser.add_argument('left')
  parser.add_argument('right')
  parser.add_argument('--bad', action='store_true')
  parser.add_argument('-p', '--padding', type=int, default=4)
  parser.add_argument('-f', '--font-family', default='sans-serif')
  parser.add_argument('-s', '--font-size', type=int, default=12)
  args = parser.parse_args(argv)

  # First compute the size of the output image.
  temp = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
  context = cairo.Context(temp)
  context.select_font_face(args.font_family)
  context.set_font_size(args.font_size)
  ext_left = context.text_extents(args.left)
  ext_right = context.text_extents(args.right)

  width = int(args.padding * 4 + ext_left[2] + ext_right[2])
  height = int(context.font_extents()[2]) + args.padding

  # Create a new surface that we can render the badge width.
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  context = cairo.Context(surf)
  context.select_font_face(args.font_family)
  context.set_font_size(args.font_size)
  context.set_source_rgb(*COLOR_LEFT)
  context.rectangle(0, 0, args.padding * 2 + ext_left[2], height)
  context.fill()
  context.set_source_rgb(*(COLOR_RIGHT_BAD if args.bad else COLOR_RIGHT_GOOD))
  context.rectangle(args.padding * 2 + ext_left[2], 0, args.padding * 2 + ext_right[2], height)
  context.fill()

  context.set_source_rgb(1.0, 1.0, 1.0)
  for i in range(3):
    context.move_to(args.padding, args.padding + rint(height / 2))
    context.show_text(args.left)
    context.move_to(args.padding * 3 + ext_left[2], args.padding + rint(height / 2))
    context.show_text(args.right)

  surf.write_to_png(args.outfile)


if require.main == module:
  sys.exit(main())
