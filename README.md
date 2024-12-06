# GitHub Actions Workflow Fail Alert

Scans running build workflows of [scrumdojo/quizmaster](https://github.com/scrumdojo/quizmaster) and plays
alert sound for each failed build.

## GitHub Access Token

Create a fine-grained access token on **Setttings / Developer settings / Personal access tokens** with repository access:

- Read access to actions and metadata

Save the token to github-token.txt

## Install dependencies

```
pip install playsound
```

If the install fails, run this (see [playsound/issues/150](https://github.com/TaylorSMarks/playsound/issues/150) for more):

```
pip install wheel
pip install setuptools
pip install playsound
```