# vim: sw=2 ai expandtab
#    __init__.py is part of the pipcache repository and oc_template module.
#    It's purpose is define the OcTemplate class that will build OpenShift
#    templates from a jinja template file.
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

from jinja2 import Template
import os

SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
TEMPLATE=SCRIPT_DIR + '/pipcache-template.yaml.j2'

class OcTemplate(object):
  def __init__(self, verbose=0, template=TEMPLATE, directory=None, templateType='persistent'):
    if directory is None:
      directory = os.getcwd()

    self.verbose=verbose
    self.template=template
    self.templateType=templateType
    self.write_template="{}/{}-{}.yaml".format(
        directory,
        os.path.basename(template).split('.')[0],
        templateType)

    self.log(3, "Arg Verbose: {}".format(verbose))
    self.log(3, "Arg template: {}".format(template))
    self.log(3, "Arg directory: {}".format(directory))
    self.log(3, "Arg templateType: {}".format(templateType))

  def log(self, v, m):
    if self.verbose >= v:
      print m

  def process(self):
    self.log(0, "templateType={}".format(self.templateType))
    self.log(1, "Reading from: {}".format(self.template))
    self.log(1, "Writing to: {}".format(self.write_template))

    raw = self.read()
    template = Template(raw)
    self.log(3, "Template read in ok.")
    raw = template.render(templateType=self.templateType)
    self.log(3, "Template rendered [{}] bytes.".format(len(raw)))
    self.write(raw)

  def read(self):
    with open(self.template, 'r') as r:
      raw = r.read()
      self.log(2, "Reading in [{}] bytes.".format(len(raw)))
      return raw

  def write(self, raw):
    with open(self.write_template, 'w') as w:
      w.write(raw)
    self.log(2, "Wrote out [{}] bytes.".format(len(raw)))
