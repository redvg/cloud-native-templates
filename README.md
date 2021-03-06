Templates & blueprints to facilitate cloud-native development efforts. Can be imported into IntelliJ and VSCode via Cloud Code plugin.

- [motivation](#motivation)
- [contents](#contents)
    - [server](#server)
    - [platform](#platform)
    - [ops](#ops)
- [IDEs](#ides)
    - [template descriptor](#template-descriptor)
    - [usage](#usage)
- [contributing](#contributing)
- [todo](#todo)


<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/><img alt="Go" src="https://img.shields.io/badge/go-%2300ADD8.svg?&style=for-the-badge&logo=go&logoColor=white"/><img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/><img alt="Docker" src="https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/><img alt="Kubernetes" src="https://img.shields.io/badge/kubernetes%20-%23326ce5.svg?&style=for-the-badge&logo=kubernetes&logoColor=white"/><img alt="Terraform" src="https://img.shields.io/badge/terraform%20-%235835CC.svg?&style=for-the-badge&logo=terraform&logoColor=white"/><img alt="FastAPI" src="https://img.shields.io/badge/fastapi%20-%2313988a.svg?&style=for-the-badge&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIgogICB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIKICAgaWQ9InN2ZzgiCiAgIHZlcnNpb249IjEuMSIKICAgdmlld0JveD0iMCAwIDYuMzQ5OTk5OSA2LjM0OTk5OTkiCiAgIGhlaWdodD0iNi4zNDk5OTk5bW0iCiAgIHdpZHRoPSI2LjM0OTk5OTltbSI+CiAgPGRlZnMKICAgICBpZD0iZGVmczIiIC8+CiAgPG1ldGFkYXRhCiAgICAgaWQ9Im1ldGFkYXRhNSI+CiAgICA8cmRmOlJERj4KICAgICAgPGNjOldvcmsKICAgICAgICAgcmRmOmFib3V0PSIiPgogICAgICAgIDxkYzpmb3JtYXQ+aW1hZ2Uvc3ZnK3htbDwvZGM6Zm9ybWF0PgogICAgICAgIDxkYzp0eXBlCiAgICAgICAgICAgcmRmOnJlc291cmNlPSJodHRwOi8vcHVybC5vcmcvZGMvZGNtaXR5cGUvU3RpbGxJbWFnZSIgLz4KICAgICAgICA8ZGM6dGl0bGU+PC9kYzp0aXRsZT4KICAgICAgPC9jYzpXb3JrPgogICAgPC9yZGY6UkRGPgogIDwvbWV0YWRhdGE+CiAgPGcKICAgICB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtODcuNTM5Mjg2LC04NC40MjYxOTEpIgogICAgIGlkPSJsYXllcjEiPgogICAgPHBhdGgKICAgICAgIGlkPSJwYXRoODE1IgogICAgICAgZD0ibSA4Ny41MzkyODYsODQuNDI2MTkxIGggNi4zNSB2IDYuMzUgaCAtNi4zNSB6IgogICAgICAgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2Utd2lkdGg6MC4yNjQ1ODMzMiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0ic3Ryb2tlLXdpZHRoOjAuMjY0NTgzMzI7ZmlsbDojZmZmZmZmIgogICAgICAgaWQ9InBhdGg4MTciCiAgICAgICBkPSJtIDkwLjcxNDI4Niw4NC45NjA2NDkgYyAtMS40NTc4NTQsMCAtMi42NDA1NDIsMS4xODI2ODggLTIuNjQwNTQyLDIuNjQwNTQyIDAsMS40NTc4NTQgMS4xODI2ODgsMi42NDA1NDIgMi42NDA1NDIsMi42NDA1NDIgMS40NTc4NTQsMCAyLjY0MDU0MiwtMS4xODI2ODggMi42NDA1NDIsLTIuNjQwNTQyIDAsLTEuNDU3ODU0IC0xLjE4MjY4OCwtMi42NDA1NDIgLTIuNjQwNTQyLC0yLjY0MDU0MiB6IG0gLTAuMTM3NTgzLDQuNzU3MjA5IHYgLTEuNjU2MjkyIGggLTAuOTIwNzUgbCAxLjMyMjkxNiwtMi41NzcwNDIgdiAxLjY1NjI5MiBoIDAuODg2MzU0IHoiIC8+CiAgPC9nPgo8L3N2Zz4K"/><img alt="GitLab" src="https://img.shields.io/badge/gitlab%20-%23181717.svg?&style=for-the-badge&logo=gitlab&logoColor=white"/><img alt="Google Cloud" src="https://img.shields.io/badge/Google%20Cloud%20-%234285F4.svg?&style=for-the-badge&logo=google-cloud&logoColor=white"/>

[![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

## Motivation

- repository serves as a one-stop catalog hub of source files which may come handy during cloud-native endeavours
- provided template can be a code snippet solving a simple task (e.g. prometheus alerting manifest) or a fully-fledged solution (e.g. well-architected gke deployment)
- functional, rather than language or technology, folder structure. functional categories are highly opinionated and are subject to review
- flat folder structure with a single root for each functional topic, and a sub-folder for each template
- repository contains not only blueprints/battle-proven/reference solutions but also technology experiments which serve as a boostrap and may experience further improvements in terms of performance and best practices

## Contents

### Server

- ![Python ASGI server (fastapi+uvicorn)](server/python-asgi) [![Maintainer](https://badgen.net/badge/maintainer/👷redvg/black)](https://github.com/redvg)

### Platform

- ![Well-architected PCI-compliant GKE](platforms/gke-wa-pci) [![Fork](https://badgen.net/badge/forked/yes/green?icon=github)](https://github.com/GoogleCloudPlatform/pci-gke-blueprint)

- ![Well-architected GKE microservices shop](platforms/gke-wa-shop) [![Fork](https://badgen.net/badge/forked/yes/green?icon=github)](https://github.com/GoogleCloudPlatform/microservices-demo)

- ![k8s Python guestbook](platforms/k8s-py-guestbook) [![Fork](https://badgen.net/badge/forked/yes/green?icon=github)](https://github.com/GoogleCloudPlatform/cloud-code-samples)

- ![k8s Golang guestbook](platforms/k8s-go-guestbook) [![Fork](https://badgen.net/badge/forked/yes/green?icon=github)](https://github.com/GoogleCloudPlatform/cloud-code-samples)

- ![k8s NodeJS guestbook](platforms/k8s-nodejs-guestbook) [![Fork](https://badgen.net/badge/forked/yes/green?icon=github)](https://github.com/GoogleCloudPlatform/cloud-code-samples)

- ![IoT on GCP](platforms/iot-gcp) [![Maintainer](https://badgen.net/badge/maintainer/👷redvg/black)](https://github.com/redvg)


### Ops

- ![GCP Cloud Build which fetches secrets from Secret Manager, builds & pushes docker image to Artifact Registry and deploys image to Cloud Run](ops/gcp-cloudbuild-cloudrun) [![Maintainer](https://badgen.net/badge/maintainer/👷redvg/black)](https://github.com/redvg)

- ![GitLab CI runner which triggers GCP Cloud Build pipeline on push](ops/gitlab-gcp-cloudbuild) [![Maintainer](https://badgen.net/badge/maintainer/👷redvg/black)](https://github.com/redvg)

- ![GitLab CI runner which provisions GCP resources with Terraform](ops/gitlab-gcp-terraform) [![Maintainer](https://badgen.net/badge/maintainer/👷redvg/black)](https://github.com/redvg)

## IDEs

### Template Descriptor

The `.cctemplate` is a [Template Descriptor](https://cloud.google.com/code/docs/intellij/set-up-template-repo#template_descriptor_schema) file that describes the contents of your repository so that Cloud Code knows where to look for your templates. It should look something like the following:

```json
{
    "metadata": {
        "version": "1"
    },
    "templates": [
        {
            "path": "path/to/my/template",
            "name": "My Template",
            "description": "This template helps you create something amazing!"
        },
        ...
    ]
}
```

You can learn more about the Template Descriptor schema [here](https://cloud.google.com/code/docs/vscode/set-up-template-repo#template_descriptor_schema).


### Usage

You can configure your IDE to recognize this repository and create applications based on the templates within. Follow the steps below to see Custom Templates in action:

1. Install Cloud Code for [IntelliJ](https://cloud.google.com/code/docs/intellij/install?utm_source=redvg17@gmail.com&utm_medium=i-want-to-become-gde) or [VS Code](https://cloud.google.com/code/docs/vscode/install?utm_source=redvg17@gmail.com&utm_medium=partner&utm_campaign=few-bucks-for-red)

2. Import the Custom Template repo on [IntelliJ](https://cloud.google.com/code/docs/intellij/create-app-from-custom-template) or [VS Code](https://cloud.google.com/code/docs/vscode/create-app-from-custom-template), using this repo's Git URL: `https://github.com/shortcut/cloud-native-templates.git`

Find out more at:
- https://cloud.google.com/code/docs/intellij/set-up-template-repo
- VSCode https://cloud.google.com/code/docs/vscode/create-app-from-custom-template 
- IntelliJ https://cloud.google.com/code/docs/intellij/create-app-from-custom-template
- https://github.com/GoogleCloudPlatform/cloud-code-custom-templates-example

## Contributing

1. Create a new directory containing your own template (or make changes to any of the sample templates)
2. If you are not originating a template make sure a license from sourced repo is included
3. Establish a feedback channel by referencing either a maintainer or a source repo in the contents section
4. Make any necessary updates to the templates in the `.cctemplate` file 
5. Import updated repository into Cloud Code
