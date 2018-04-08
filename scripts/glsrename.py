#!/usr/bin/env python3
# Copyright (C) 2016 Niklas Rosenstein
# All rights reserved.
#
# created: 2016/01/08
# last modified: 2016/01/08

import os
import glob
import re
import sys

from os import listdir
from datetime import datetime

expr = 'AZG82175065(0[01])_[0-9]{3}_([0-9]{8})\.pdf'


def main(argv=None, prog=None):
  files_renamed = 0
  for name in listdir('.'):
    match = re.match(expr, name)
    if not match:
      if name.endswith('.pdf'):
        print('warn: {0} is a PDF but does not seem to be from the GLS'.format(name))
      continue
    account, date = match.groups()
    date = datetime.strptime(date, '%Y%m%d').date()
    new_name = 'GLS{0}_{1}_{2:0>2}_{3:0>2}.pdf'.format(account, date.year, date.month, date.day)
    os.rename(name, new_name)
    print('info: renamed {0} to {1}'.format(name, new_name))
    files_renamed += 1
  if not files_renamed:
    print('no files renamed.')


if require.main == module:
  sys.exit(main())
