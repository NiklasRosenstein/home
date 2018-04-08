#!/usr/bin/env python3
#
# Copyright (C) 2016  Niklas Rosenstein
# All rights reserved.

import os
import sys
import re
import subprocess
import configparser


def main(argv=None, prog=None):
  parser = configparser.ConfigParser()
  parser.read('.gitmodules')
  for section in parser.sections():
    subpath = re.match('submodule\s+"(.+)"', section).group(1)
    url = parser.get(section, 'url')
    path = parser.get(section, 'path')
    if path != subpath:
      sys.exit('Error: submodule "{0}" path does not match: {1}'.format(subpath, path))

    res = subprocess.call(['git', 'submodule', 'add', url, path])


if require.main == module:
  sys.exit(main())
