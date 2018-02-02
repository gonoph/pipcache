# pipcache
Repository to generate an OpenShift BuildConfig for devpi-server to act as a
caching server for PyPI upstream.

# Purpose
I was spending too much time waiting for pip downloads when I was testing my
python builds in OpenShift. I got an idea based on these blogs:

* <http://www.machint.com/articles/2014/03/pypi-caching-mirror-devpi.html>
* <https://blog.openshift.com/using-image-source-reduce-build-times/>

Finally, I decided that I needed a caching server for PyPi. So, this is what I
did.

# Usage

Clone the repository.

```bash
git clone https://github.com/gonoph/pipcache.git
```

Install the Template if you want

```bash
# enter your project first
oc project $YOUR_NAMESPACE

# or create your project/namespace first
oc new-project my_namespace

# install the templates
oc create -f pipcache-template-ephemeral.yaml # for ephemeral
oc create -f pipcache-template-persistent.yaml # for persistent

# or install it in the openshift namespace for everyone to use
oc create -f pipcache-template-persistent.yaml -n openshift
```

Process the template or the use the GUI to install it

```bash
# if you don't use the GUI, process the template
oc process pipcache-template-persistent -p VOLUME_CAPACITY=2Gi | oc create -f -

# or process the file directly if you didn't install it
oc process -f pipcache-template-persistent.yaml -p VOLUME_CAPACITY=512Mi | oc create -f -

# or just create the resource file to look at it
oc process pipcache-template-persistent > resources.yaml

# then install it if you did the above command
oc create -f resources.yaml

# optionally patch the BuildConfig or DeploymentConfig to only run build or deploy on certain nodes:
oc patch  bc/pipcache -p '{"spec":{"nodeSelector":{"speed":"fast"}}}'
oc patch  dc/pipcache -p '{"spec":{"template":{"spec":{"nodeSelector":{"speed":"fast"}}}}}'
```

Or just patch the current project to default to a node selector using this [hard to find annotation][2].
```bash
oc patch ns/$(oc project -q) -p '{"metadata":{"annotations":{"openshift.io/node-selector":"speed=fast"}}}'
```

To use it set this environment variable for your s2i builds as [described in the upstream][1].

* `PIP_INDEX_URL` - Set this variable to use a custom index URL or mirror to download required packages during build proc.

[1]: https://github.com/sclorg/s2i-python-container/tree/master/2.7
[2]: https://blog.openshift.com/deploying-applications-to-specific-nodes/

# Parameters

[Checkout the Parameters Page](Parameters.md)

# Finding the right URL

There's two ways to access the devpi-server url:

1. Externally for everyone outside the cluster using the OpenShift pipcache router endpoint.
2. Internally for pods inside the cluster using the pipcache service endpoint.

Here's how to find both:

```bash
# replace pipcache with the NAME of the app if you changed defaults
NAME=pipcache
# for the external end point:
echo $(oc get route $NAME -o jsonpath=https://{.spec.host}{.spec.path}root/pypi)

# for the internal end point:
echo $(oc get svc $NAME -o jsonpath=http://{.spec.clusterIP}:{.spec.ports[0].port}/root/pypi)
```

Example:

```bash
$ echo $(oc get route $NAME -o jsonpath=https://{.spec.host}{.spec.path}root/pypi)
https://pipcache-infra.apps.example.com/root/pypi
$ curl -s https://pipcache-infra.apps.example.com/root/pypi
```

Yields this output

```json
{
  "type": "indexconfig",
  "result": {
    "volatile": false,
    "mirror_url": "https://pypi.python.org/simple/",
    "mirror_web_url_fmt": "https://pypi.python.org/pypi/{name}",
    "type": "mirror",
    "title": "PyPI",
    "projects": [
// snip //
    ]
  }
}
```

# License
Copyright (C) 2018  Billy Holmes

Released and Licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

```
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
