#!/usr/bin/env python3

from datetime import datetime
from itertools import chain
from pathlib import Path

import argparse
import exifread
import os
import sys

def reprint(*msg, sep=' ', end='\n', file=None):
  print('\033[K' + sep.join(map(str, msg)), end=end, file=file)

def enable_ansii_terminal_support():
  try:
    import colorama; colorama.init()
    return True
  except ImportError:
    if os.name == 'nt':
      import ctypes
      kernel32 = ctypes.windll.kernel32
      kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
      return True
  return False

def iter_dir(dirname):
  for filename in os.listdir(dirname):
    yield os.path.join(dirname, filename)

def main(argv=None, prog=None):
  parser = argparse.ArgumentParser(prog=prog)
  parser.add_argument('-d', '--dry', action='store_true')
  parser.add_argument('files', nargs='*')
  parser.add_argument('-D', '--directory', action='append', default=[])
  parser.add_argument('-S', '--suffix', action='append', default=[])
  parser.add_argument('-F', '--format', default='%Y%m%d_%H%M%S')
  parser.add_argument('-q', '--quiet', action='count', default=0)
  parser.add_argument('--allow-mtime-fallback', action='store_true')
  args = parser.parse_args(argv)

  enable_ansii_terminal_support()

  suffixes = []
  for string in args.suffix:
    suffixes += filter(bool, string.upper().split(','))

  iterators = [args.files] + [iter_dir(x) for x in args.directory]
  files = list(map(Path, chain.from_iterable(iterators)))

  for filename in files:
    if os.path.isdir(filename):
      continue
    if suffixes and not any(filename.suffix.upper() == x for x in suffixes):
      continue
    # Stat to reset the modification time after changing the filename.
    stat = filename.stat()

    if filename.suffix.upper() not in ('.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF', '.GIF'):
      if args.quiet < 1:
        print('{}: Unsupported file suffix'.format(filename), end='\n', file=sys.stderr)
      continue

    # Read the EXIF tags and extract the DateTimeOriginal tag.
    with open(filename, 'rb') as fp:
      tags = exifread.process_file(fp)
    if not tags:
      if args.quiet < 1:
        reprint('{}: no EXIF tags at all'.format(filename), end='\n', file=sys.stderr)
      continue

    date_tag = tags.get('EXIF DateTimeOriginal') or \
              tags.get('Image DateTimeOriginal') or \
              tags.get('DateTimeOriginal')

    # Parse the date, and default to the modification time if appropriate.
    if date_tag:
      try:
        date = datetime.strptime(str(date_tag), '%Y:%m:%d %H:%M:%S')
      except ValueError as e:
        date = None
        if args.quiet < 1:
          print('{}: {}'.format(filename, e), end='\n', file=sys.stderr)
    else:
      date = None
    if not date and args.allow_mtime_fallback:
      date = datetime.fromtimestamp(filename.stat().st_mtime)
    elif not date:
      if args.quiet < 1:
        reprint('{}: no DateTimeOriginal Tag'.format(filename), end='\n', file=sys.stderr)
      continue

    # Determine the new filename, and resolve duplicate names by enumerating
    # a four character-wide index. Note that we may find the exact same file
    # as the input file again, in which case we can skip this file.
    new_stem = date.strftime(args.format)
    new_filename = Path(filename.parent, new_stem + filename.suffix)
    is_samefile = False

    index, temp = 1, new_filename
    while os.path.exists(temp):
      if temp == filename:
        is_samefile = True
        break
      temp = Path(new_filename.parent, new_filename.stem + '_{:0>4d}'.format(index) + new_filename.suffix)
      index += 1
    new_filename = temp

    if is_samefile:
      if args.quiet < 1:
        print('{}: skipped'.format(filename))
      continue

    if args.quiet < 2:
      reprint('{} => {}'.format(filename, new_filename))

    if not args.dry:
      try:
        os.rename(filename, new_filename)
      except FileExistsError as e:
        reprint(e, end='\n', file=sys.stderr)
      else:
        # Reset the modification and access times.
        os.utime(new_filename, (stat.st_atime, stat.st_mtime))


if require.main == module:
  sys.exit(main())
