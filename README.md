# cloud-native-templates
Templates to facilitate cloud-native development efforts. Can be imported into IntelliJ and VSCode via Cloud Code plugin.

- [contents](#contents)
- [IDEs](#ides)
    - [template descriptor](#template-descriptor)
    - [usage](#usage)
- [contributing](#contributing)
- [references](#references)
- [todo](#todo)


<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/><img alt="Go" src="https://img.shields.io/badge/go-%2300ADD8.svg?&style=for-the-badge&logo=go&logoColor=white"/><img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/><img alt="Docker" src="https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/><img alt="Kubernetes" src="https://img.shields.io/badge/kubernetes%20-%23326ce5.svg?&style=for-the-badge&logo=kubernetes&logoColor=white"/><img alt="Terraform" src="https://img.shields.io/badge/terraform%20-%235835CC.svg?&style=for-the-badge&logo=terraform&logoColor=white"/><img alt="FastAPI" src="https://img.shields.io/badge/fastapi%20-%2313988a.svg?&style=for-the-badge&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIgogICB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIKICAgaWQ9InN2ZzgiCiAgIHZlcnNpb249IjEuMSIKICAgdmlld0JveD0iMCAwIDYuMzQ5OTk5OSA2LjM0OTk5OTkiCiAgIGhlaWdodD0iNi4zNDk5OTk5bW0iCiAgIHdpZHRoPSI2LjM0OTk5OTltbSI+CiAgPGRlZnMKICAgICBpZD0iZGVmczIiIC8+CiAgPG1ldGFkYXRhCiAgICAgaWQ9Im1ldGFkYXRhNSI+CiAgICA8cmRmOlJERj4KICAgICAgPGNjOldvcmsKICAgICAgICAgcmRmOmFib3V0PSIiPgogICAgICAgIDxkYzpmb3JtYXQ+aW1hZ2Uvc3ZnK3htbDwvZGM6Zm9ybWF0PgogICAgICAgIDxkYzp0eXBlCiAgICAgICAgICAgcmRmOnJlc291cmNlPSJodHRwOi8vcHVybC5vcmcvZGMvZGNtaXR5cGUvU3RpbGxJbWFnZSIgLz4KICAgICAgICA8ZGM6dGl0bGU+PC9kYzp0aXRsZT4KICAgICAgPC9jYzpXb3JrPgogICAgPC9yZGY6UkRGPgogIDwvbWV0YWRhdGE+CiAgPGcKICAgICB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtODcuNTM5Mjg2LC04NC40MjYxOTEpIgogICAgIGlkPSJsYXllcjEiPgogICAgPHBhdGgKICAgICAgIGlkPSJwYXRoODE1IgogICAgICAgZD0ibSA4Ny41MzkyODYsODQuNDI2MTkxIGggNi4zNSB2IDYuMzUgaCAtNi4zNSB6IgogICAgICAgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2Utd2lkdGg6MC4yNjQ1ODMzMiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0ic3Ryb2tlLXdpZHRoOjAuMjY0NTgzMzI7ZmlsbDojZmZmZmZmIgogICAgICAgaWQ9InBhdGg4MTciCiAgICAgICBkPSJtIDkwLjcxNDI4Niw4NC45NjA2NDkgYyAtMS40NTc4NTQsMCAtMi42NDA1NDIsMS4xODI2ODggLTIuNjQwNTQyLDIuNjQwNTQyIDAsMS40NTc4NTQgMS4xODI2ODgsMi42NDA1NDIgMi42NDA1NDIsMi42NDA1NDIgMS40NTc4NTQsMCAyLjY0MDU0MiwtMS4xODI2ODggMi42NDA1NDIsLTIuNjQwNTQyIDAsLTEuNDU3ODU0IC0xLjE4MjY4OCwtMi42NDA1NDIgLTIuNjQwNTQyLC0yLjY0MDU0MiB6IG0gLTAuMTM3NTgzLDQuNzU3MjA5IHYgLTEuNjU2MjkyIGggLTAuOTIwNzUgbCAxLjMyMjkxNiwtMi41NzcwNDIgdiAxLjY1NjI5MiBoIDAuODg2MzU0IHoiIC8+CiAgPC9nPgo8L3N2Zz4K"/><img alt="React" src="https://img.shields.io/badge/react%20-%2320232a.svg?&style=for-the-badge&logo=react&logoColor=%2361DAFB"/><img alt="Material UI" src="https://img.shields.io/badge/material%20ui%20-%230081CB.svg?&style=for-the-badge&logo=material-ui&logoColor=white"/>

[![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)


## contents

- Flat & functional: this repo follows functional, rather than language or technology, folder structure. Also a flat folder structure with a single root for each functional topic, and a sub-folder for each template.
- Battle-proven & experiment: provided template should work as is. It may though experience further improvements in terms of performance and best practices.  

### server

- ![Python ASGI server (fastapi served over uvicorn)](server/python-asgi)

### client
### platforms
runtimes & service providers e.g public clouds (gcp, azure),  aaS (hashicorp cloud), container orchestration (k8s, rke, nomad)

### ops
cicd, testing, monitoring..

- ![GCP Cloud Build which fetches secrets from Secret Manager, builds & pushes docker image to Artifact Registry and deploys image to Cloud Run](ops/gcp-cloudbuild-cloudrun)
- ![GitLab CI runner which triggers GCP Cloud Build pipeline on push](ops/gitlab-gcp-cloudbuild)

## IDEs

### template descriptor

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

There is an example `.cctemplate` file in this repository that you can review, and you can learn more about the Template Descriptor schema [here](https://cloud.google.com/code/docs/vscode/set-up-template-repo#template_descriptor_schema).

### usage

You can configure your IDE to recognize this repository and create applications based on the templates within. Follow the steps below to see Custom Templates in action:

1. Install Cloud Code for [IntelliJ](https://cloud.google.com/code/docs/intellij/install?utm_source=redvg17@gmail.com&utm_medium=i-want-to-become-gde) or [VS Code](https://cloud.google.com/code/docs/vscode/install?utm_source=redvg17@gmail.com&utm_medium=partner&utm_campaign=few-bucks-for-red)

2. Import the Custom Template repo on [IntelliJ](https://cloud.google.com/code/docs/intellij/create-app-from-custom-template) or [VS Code](https://cloud.google.com/code/docs/vscode/create-app-from-custom-template), using this repo's Git URL: `https://github.com/shortcut/cloud-native-templates.git`

## contributing

1. Create a new directory containing your own template (or make changes to any of the sample templates)
2. Make any necessary updates to the templates in the `.cctemplate` file 
3. Add a badge to `README.md` :)
3. Import updated repository into Cloud Code  

## references

- https://cloud.google.com/code/docs/intellij/set-up-template-repo
- VSCode https://cloud.google.com/code/docs/vscode/create-app-from-custom-template 
- IntelliJ https://cloud.google.com/code/docs/intellij/create-app-from-custom-template
- https://github.com/GoogleCloudPlatform/cloud-code-custom-templates-example

## todo
- [x] python asgi
- [ ] golang gorilla
- [ ] golang http2 grpc
- [ ] react
- [ ] prometheus
- [ ] k8s
- [ ] nodejs
- [ ] expressjs
- [ ] rust
- [ ] dart
- [ ] flutter
- [ ] circleci
- [x] gcp cloud build cloud run cd
- [x] gitlab ci
- [ ] github actions
- [ ] rancher
- [ ] nomad
- [ ] azure arm
- [ ] load generator
- [ ] k6
