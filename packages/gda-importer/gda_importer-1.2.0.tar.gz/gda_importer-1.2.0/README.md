# GDA Importer

GDA Importer contains simple utilities that are helpful for installation and CI/CD of python packages.  Install with 

```bash
pip install -U gda-importer
```

and use the scripts `ppinfo` and `pull-private-deps`, described below.
The only dependencies are [toml](https://pypi.org/project/toml/) and [packaging](https://pypi.org/project/packaging/).

## ppinfo

`ppinfo` reads the contents of `pyproject.toml` files. It can be accessed as `python -m gda_importer.ppinfo` or as the installed script `ppinfo`.

Run `ppinfo -h` for details.

## pull-private-deps

`pull-private-deps` installs dependencies specified in a `private-deps.toml` by whatever means necessary.

**Why**?  We at GDA have many internal packages that are developed privately and require authentication. Unfortunately, it is not possible to give this specification in `pyproject.toml` or `environment.yml` because those sources do not provide authentication for private repositories. The `pull-private-deps.py` script allows us to install our code in different environments easily. **If [PEP 708](https://peps.python.org/pep-0708/#alternate-locations-metadata) is ever finished, this will become uneccesary.**

### Authentication Fall-Back

The logic in `pull-private-deps` handles the following cases.

1. If `--local` is specified, then the parent directory will be searched for a repository with the expected name, and `pip -e ../dirname` will be used on that directory.
2. If `--clone` is specified, then the repository will be cloned in the parent directory, for later use by `--local`.
3. If in a Kaniko docker builder image, presumably within a CI runner, use `CI_JOB_TOKEN` from the environment. Note that you **also** need to give this project permission in the *other* project's Job Token Access list, under the CI/CD Settings menu. This will result in an authenticated HTTPS command.
4. If in a GitLab CI job, use the specified `token_var`, which defaults to `CI_JOB_TOKEN`. If using the default, you **also** need to give this project permission in the *other* project's Job Token Access list, under the CI/CD Settings menu.  Otherwise, you need to make a Project Token and share it as a masked variable. This will result in an authenticated HTTPS command.
5. If on a workstation, where the variable set by `token_var=TOKEN_VAR_NAME` is defined (defaults to `CI_JOB_TOKEN`) in your environmental variables (for example, `TOKEN_VAR_NAME="glpat-XXXX" ./pull-private-deps.py`), use an authenticated HTTPS command.
6. If on a workstation, where the variable set by `token_var=TOKEN_VAR_NAME` is **not** defined (defaults to `CI_JOB_TOKEN`) in your environmental variables, use SSH.  SSH will fail if your SSH keys aren't loaded properly.

### Private-Deps Options

The `private-deps.toml` file has stanzas for each dependency.
The options in each stanza lead to different installation commands.
Let's examine each of these cases.

#### Simple Case

```toml
["example-package[option1,option2]"]
  gitlab_host = "gitlab.example.com"
  gitlab_path = "groupname/projectname"
```

If `CI_JOB_TOKEN` is available, this results in pulling a wheel over HTTPS.

```bash
pip install -v example-package[option1,option2] --index-url https://gitlab-ci-token:$CI_JOB_TOKEN@gitlab.example.com/api/v4/projects/groupname%2Fprojectname/packages/pypi/simple
```

If `CI_JOB_TOKEN` is missing, this results in pulling source over SSH.

```bash
pip install -v example-package[option1,option2]@git+ssh://git@gitlab.example.com/groupname/projectname.git
```

#### Version Set

Use `version_set` to specify a specific version or range of versions for installation of prebuilt wheels from a PyPI-style registry.

```toml
["example-package[option1,option2]"]
  gitlab_host = "gitlab.example.com"
  gitlab_path = "groupname/projectname"
  version_set = ">=1.0,<3.0"
```

If `CI_JOB_TOKEN` is available, this results in pulling a wheel over HTTPS, with pip checking versions.

```bash
pip install -v example-package[option1,option2]<3.0,>=1.0 --index-url https://gitlab-ci-token:$CI_JOB_TOKEN@gitlab.example.com/api/v4/projects/groupname%2Fprojectname/packages/pypi/simple
```

If `CI_JOB_TOKEN` is missing, this results in pulling source over SSH, and `version_set` will be ignored.

```bash
pip install -v example-package[option1,option2]@git+ssh://git@gitlab.example.com/groupname/projectname.git
```

#### Force Src

If `force_src = true`, then a `gitlab_spec` must be specified, and `version_set` is irrelevant.
Use `gitlab_spec` to specify a specifig git reference for installation from source.

```toml
["example-package[option1,option2]"]
  gitlab_host = "gitlab.example.com"
  gitlab_path = "groupname/projectname"
  force_src = true
  gitlab_spec = "branch-or-commit-or-tag-ref"
```

If `CI_JOB_TOKEN` is available, this results in pulling source over HTTPS.

```bash
pip install -v example-package[option1,option2]@git+https://gitlab-ci-token:$CI_JOB_TOKEN@gitlab.example.com/groupname/projectname.git@branch-or-commit-or-tag-ref
```

If `CI_JOB_TOKEN` is missing, this results in pulling source over SSH.

```bash
pip install -v example-package[option1,option2]@git+ssh://git@gitlab.example.com/groupname/projectname.git@branch-or-commit-or-tag-ref
```

#### `version_set` versus `gitlab_spec`

The `version_set` option is for version sets given by pip-style conditions.  This only applies to package registries with the `force_src = false` option.

The `gitlab_spec` option is for gitlab references (branch names, commit hashes, tags) and only applies if `force_src = true`.

If `gitlab_spec` and `version_set` are both specified and `force_src = true`, then to avoid confusion they are checked for consistency. If `gitlab_spec` looks like a semantic version (for example, the tag `v3.0.1`), it will be checked against `version_set`, and a warning will be issued if they do not match.

```toml
["example-package[option1,option2]"]
  gitlab_host = "gitlab.example.com"
  gitlab_path = "groupname/projectname"
  gitlab_spec = "v3.0.1"
  version_set = ">=1.0,<3.0"
```

`ValueError: Version implied by gitlab_spec is not included in the version_set.`

#### Caveats

- Package name must satisfy  [PyPA guidelines](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#names)
- Extra options must satisfy [PyPA guidelines](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#extras)

- `pip install` on your main package will be **unaware** of these dependencies, because these private-repository dependencies are installed after the other types of dependencies, and must be re-installed for each job in the CI/CD pipeline.
Therefore, for pipeline efficiency, *you should make sure that [pyproject.toml](pyproject.toml) or [environment.yml](environment.yml) contain whatever second-order public dependencies will be needed.*

- If any of the included private dependencies have any **Anaconda Binary Dependencies** (see the next section), then these binary dependencies **must be manually added** to [environment.yml](environment.yml).

### Note Possible `conda` Dependencies

Regardless of how you follow the User Installation subsection below, be sure to check if there are any additional, `conda`-specific requirements for the package specified in `environment.yml`.

If there are any dependencies there other than the [cookiecutter defaults](https://gitlab.geomdata.com/geomdata/gda-cookiecutter/-/blob/master/environment.yml?ref_type=heads), then these may be important to include in a working conda environment wherever you intend to use this package. If there are no additional dependencies there, then this step can be disregarded.
