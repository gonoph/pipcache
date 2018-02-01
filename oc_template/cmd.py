#!/usr/bin/env python2.7
# vim: sw=2 ai expandtab
#    cmd.py is part of the pipcache repository and oc_template module. It's
#    purpose is to execute the module as a command.
#
#    Copyright (C) 2018  Billy Holmes
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from oc_template import TEMPLATE,OcTemplate

if __name__ == '__main__':
  import argparse
  import os
  cwd=os.getcwd()
  parser = argparse.ArgumentParser(description='Write out OpenShift template from jinja2 template.')
  parser.add_argument('-v', '--verbose', help='increase verbosity', action='count')
  parser.add_argument('-t', '--template', help='the template file (default: {})'.format(TEMPLATE), default=TEMPLATE)
  parser.add_argument('-d', '--directory', '--dir', help='the output directory (default: cwd({}))'.format(cwd), default=cwd)
  parser.add_argument('templateType', nargs=1, help='the template type', choices=['persistent', 'ephemeral'])
  args = parser.parse_args()
  OcTemplate(args.verbose, args.template, args.directory, args.templateType[0]).process()
