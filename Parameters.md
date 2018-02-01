# Parameters List

These are the parameters for each of the templates: `pipcache-ephemeral`, `pipcache-persistent`


# Template: `pipcache-ephemeral`

| Name | required | default | description |
| ---- | -------- | ------- | ----------- |
| `NAME` | True | pipcache | The name assigned to all of the frontend objects defined in this template. |
| `NAMESPACE` | True | openshift | The OpenShift Namespace where the builder ImageStream resides. |
| `MEMORY_LIMIT` | True | 128Mi | Maximum amount of memory the container can use. |
| `CPU_LIMIT` | True | 1 | Maximum amount of CPU the container can use (in cores). |
| `DATA_VOLUME` | True | /opt/app-root/data | Data volume path |
| `SOURCE_REPOSITORY_URL` | True | http://git.virt.gonoph.net/git/Openshift/pipcache.git | The URL of the repository with your application source code. |
| `SOURCE_REPOSITORY_REF` |  |   | Set this to a branch name, tag or other ref of your repository if you are not using the default branch. |
| `CONTEXT_DIR` |  | src | Set this to the relative path to your project if it is not in the root of your repository. |
| `APPLICATION_DOMAIN` |  |   | The exposed hostname that will route to the pipcache service, if left blank a value will be defaulted. |
| `GITHUB_WEBHOOK_SECRET` |  |   | Github trigger secret.  A difficult to guess string encoded as part of the webhook URL.  Not encrypted. |



# Template: `pipcache-persistent`

| Name | required | default | description |
| ---- | -------- | ------- | ----------- |
| `NAME` | True | pipcache | The name assigned to all of the frontend objects defined in this template. |
| `NAMESPACE` | True | openshift | The OpenShift Namespace where the builder ImageStream resides. |
| `MEMORY_LIMIT` | True | 128Mi | Maximum amount of memory the container can use. |
| `CPU_LIMIT` | True | 1 | Maximum amount of CPU the container can use (in cores). |
| `DATA_VOLUME` | True | /opt/app-root/data | Data volume path |
| `VOLUME_CAPACITY` | True | 1Gi | Volume space available for data, e.g. 512Mi, 2Gi |
| `SOURCE_REPOSITORY_URL` | True | http://git.virt.gonoph.net/git/Openshift/pipcache.git | The URL of the repository with your application source code. |
| `SOURCE_REPOSITORY_REF` |  |   | Set this to a branch name, tag or other ref of your repository if you are not using the default branch. |
| `CONTEXT_DIR` |  | src | Set this to the relative path to your project if it is not in the root of your repository. |
| `APPLICATION_DOMAIN` |  |   | The exposed hostname that will route to the pipcache service, if left blank a value will be defaulted. |
| `GITHUB_WEBHOOK_SECRET` |  |   | Github trigger secret.  A difficult to guess string encoded as part of the webhook URL.  Not encrypted. |


