#    Makefile exists as part of the pipcache repository.
#    It's used to help generate the OpenShift templates from a single source.
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
.PHONY: all start-build persistent ephemeral parameters clean 

NAME        ?= pipcache
TEMPLATE    := ./generator/templates/pipcache-template.yaml.j2
MD_TEMPLATE := ./generator/templates/Parameters.md.j2

PERSISTENT_YAML := pipcache-template-persistent.yaml
EPHEMERAL_YAML  := pipcache-template-ephemeral.yaml
PARAMETER_MD    := Parameters.md

YAML_FILES := $(PERSISTENT_YAML) $(EPHEMERAL_YAML)

help:
	@echo "usage: make (help | all | persistent | ephemeral | start-build)"
	@echo "  help        - this help"
	@echo "  all         - create both persistent and ephemral templates"
	@echo "  persistent  - create the persistent template that requests a VolumeClaim"
	@echo "  ephemeral   - create the ephemeral template that uses an empty dir"
	@echo "  parameters  - create the Parameter.md based on the yaml templates"
	@echo "  start-build - manually start a build process using the current source"
	@echo "  clean       - clean up generated yaml files"

all: persistent ephemeral parameters

persistent: $(PERSISTENT_YAML)
ephemeral: $(EPHEMERAL_YAML)
parameters: $(PARAMETER_MD)

$(PERSISTENT_YAML): $(TEMPLATE)
$(PERSISTENT_YAML): TYPE=persistent
$(EPHEMERAL_YAML): $(TEMPLATE)
$(EPHEMERAL_YAML): TYPE=ephemeral
$(PARAMETER_MD): $(MD_TEMPLATE)

$(YAML_FILES):
	@python -mgenerator.openshift -vv $(TYPE)

$(PARAMETER_MD):
	@python -mgenerator.parameters -vv $(YAML_FILES)

start-build:
	oc start-build $(NAME) --from-dir=src

clean:
	rm -fv $(YAML_FILES) $(PARAMETER_MD)
