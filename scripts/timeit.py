#!/usr/bin/env python

from __future__ import print_function
import sys
import time
import subprocess


def main(argv=None, prog=None):
  if argv is None:
    argv = sys.argv[1:]
  if not argv:
    print('fatal: missing command', file=sys.stderr)
    return 1

  tstart = time.time()
  res = subprocess.call(argv, shell=True)
  tdelta = time.time() - tstart

  print()
  print("time: {0:f}s".format(tdelta))
  return res


if require.main == module:
  sys.exit(main())
