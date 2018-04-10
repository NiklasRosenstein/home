#!/usr/bin/env python

from os.path import expanduser, join

import argparse
import logging
import errno
import ctypes
import os
import shutil
import sys

if sys.version_info[0] == 2:
  _binary_type = str
  _text_type = unicode
else:
  _binary_type = bytes
  _text_type = str


def enc(x, encoding='utf8'):
  if isinstance(x, _binary_type):
    return x.decode(encoding)
  return x


def makedirs(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno != errno.EEXIST:
      raise

def symlink(source, link_name, force=False, copy=False):
  source = os.path.abspath(expanduser(source))
  if not os.path.exists(source):
    logging.error('source "{}" does not exist'.format(source))
    return False

  link_name = os.path.abspath(expanduser(link_name))
  if os.path.lexists(link_name):
    if not force:
      logging.warn('"{}" already exists, SKIP'.format(link_name))
      return False
    if os.path.isfile(link_name) or os.path.islink(link_name):
      os.unlink(link_name)
    else:
      shutil.rmtree(link_name)

  logging.info('{} "{}" ==> "{}"'.format('Copy' if copy else 'Link', link_name, source))
  makedirs(os.path.dirname(link_name))
  if copy:
    shutil.copy2(source, link_name)
  else:
    if os.name == 'nt':
      kdll = ctypes.windll.LoadLibrary("kernel32.dll")
      res = kdll.CreateSymbolicLinkW(enc(link_name), enc(source), 1 if os.path.isdir(source) else 0)
      if res in (0, 1280):
        raise ctypes.WinError(res)#"could not link '{0}' ==> '{0}'".format(link_name, source))
    else:
      os.symlink(source, link_name)
  return True

def link_directory_contents(directory, target, force):
  for base in os.listdir(directory):
    path = join(directory, base)
    target_path = join(target, base)
    if os.path.isdir(path):
      link_directory_contents(path, target_path, force=force)
    else:
      symlink(path, target_path, force=force)

def main():
  logging.basicConfig(level=logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--force', action='store_true')
  parser.add_argument('--copy-gitconfig', action='store_true')
  parser.add_argument('-P', '--profiles-only', action='store_true')
  args = parser.parse_args()

  platform_name_choices = []
  if sys.platform.startswith('win'):
    platform_name_choices += ['win']
    config_dir = '~/AppData/Roaming'
    logging.info('Detected Windows, config_dir={}'.format(config_dir))
  elif sys.platform.startswith('darwin'):
    platform_name_choices += ['unix', 'mac']
    config_dir = '~/Library/Application Support'
    platform_name = 'win'
    logging.info('Detected macOS, config_dir={}'.format(config_dir))
  else:
    platform_name_choices += ['unix', 'linux']
    config_dir = '~/.config'
    logging.info('Detected Linux, config_dir={}'.format(config_dir))

  # Link user profiles.
  symlink('config/.gitconfig', '~/.gitconfig', force=args.force, copy=args.copy_gitconfig)
  for name in platform_name_choices:
    if os.path.isfile('config/.gitconfig.' + name):
      symlink('config/.gitconfig.' + name, '~/.gitconfig.local', force=args.force, copy=args.copy_gitconfig)
  symlink('config/.profile', '~/.profile', force=args.force)
  symlink('config/.hyper.js', '~/.hyper.js', force=args.force)
  symlink('config/jupyter/nbconfig/notebook.json', '~/.jupyter/nbconfig/notebook.json', force=args.force)
  if args.profiles_only:
    return

  # Link VS Code settings.
  symlink('config/vscode/settings.json', join(config_dir, 'Code/User/settings.json'), force=args.force)

  if os.name == 'nt':
    # Link Cmder conemu-maximus5 settings.
    symlink('config/ConEmu.xml', '~/Applications/Cmder/vendor/conemu-maximus5/ConEmu.xml', force=args.force)

  # Link Franz preferences from the Nextcloud synchronization folder.
  symlink('~/Nextcloud/share/prefs/Franz/Plugins', join(config_dir, 'Franz/Plugins'), force=args.force)
  symlink('~/Nextcloud/share/prefs/Franz/settings', join(config_dir, 'Franz/settings'), force=args.force)


if __name__ == '__main__':
  main()
