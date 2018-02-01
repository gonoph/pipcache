# vim: sw=2 ai expandtab
#    __init__.py is part of the pipcache repository and template module.
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

import jinja2
import os, logging

SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
TEMPLATE=SCRIPT_DIR + '/pipcache-template.yaml.j2'
MD_TEMPLATE=SCRIPT_DIR + "/Parameters.md.j2"

VERBOSE_TO_LOGLEVEL={
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG
    }

def ternary(value, true_value, false_value):
  return value if true_value else false_value

class BaseTemplate(object):
  def __init__(self, template_file, directory=None):
    self.logger = logging.getLogger(self.__class__.__name__)
    if directory is None:
      directory = os.getcwd()

    self.template_file = template_file
    self.directory = directory

    self.logger.debug("Arg template_file: {}".format(template_file))
    self.logger.debug("Arg directory: {}".format(directory))

  def get_output_file(self):
    # get rid of the .j2 extension
    filename = '.'.join(os.path.basename(self.template_file).split('.')[:-1])
    # add directory to path
    ret = '/'.join([self.directory, filename])
    self.logger.debug("Return args: {}".format(ret))
    return ret

  def get_template_variables(self):
    raise Exception('Not Implemented')

  def process(self):
    self.output_file = self.get_output_file()

    self.logger.warn("Reading from: {}".format(self.template_file))
    self.logger.warn("Writing to: {}".format(self.output_file))

    env = jinja2.Environment(
        loader=jinja2.PackageLoader('templates', '.')
        )
    env.filters['ternary'] = ternary

    template = env.get_template(self.template_file)

    self.logger.debug("Template read in ok.")

    variables = self.get_template_variables()
    raw = template.render(variables)

    self.logger.debug("Template rendered [{}] bytes.".format(len(raw)))
    self.write(raw)

  def write(self, raw):
    with open(self.output_file, 'w') as w:
      w.write(raw)
    self.logger.info("Wrote out [{}] bytes.".format(len(raw)))

class MdTemplate(BaseTemplate):
  def __init__(self, directory=None, oc_templates=[]):
    super(MdTemplate, self).__init__(MD_TEMPLATE, directory)

    self.oc_templates = oc_templates
    self.logger.debug("Arg oc_templates: %s", oc_templates)

  def read_yaml(self):
    import yaml
    ret = {}
    for tf in self.oc_templates:
      self.logger.warn("Reading in parameters from: %s", tf)
      data = ''
      with open(tf, 'r') as stream:
        data = yaml.load(stream)

      ret[data['metadata']['name']] = data

    self.logger.debug("Returning: %s", ret)
    return ret

  def get_template_variables(self):
    return dict(templates = self.read_yaml())

class OcTemplate(BaseTemplate):
  def __init__(self, template_file=TEMPLATE, directory=None, templateType='persistent'):
    super(OcTemplate, self).__init__(template_file, directory)

    self.templateType = templateType
    self.logger.debug("Arg templateType: {}".format(templateType))

  def get_output_file(self):
    bn = os.path.basename(self.input_file).split('.')
    # add template type
    filename = "{}-{}".format(bn[0], self.templateType)
    # add the real ext back in
    filename = '.'.join([filename, bn[1:-1] ])
    # add directory to path
    ret = '/'.join([ self.directory, filename ])
    self.logger.debug("Return args: {}".format(ret))
    return ret

  def output_template_args(self):
    bn = os.path.basename(self.template_file).split('.')
    ret = '.'.join(["{}-{}".format(bn[0], self.templateType)] + bn[1:-1])
    self.logger.debug("Will Return: {}".format(ret))
    return ret

  def get_template_variables(self):
    return dict(templateType = self.templateType)
