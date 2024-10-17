#!/bin/env python3

r"""Pull private deps by whatever means necessary.

This standalone script is Geometric Data Analytics (c) 2024, available under AGPLv3,
regardless of the other contents of the package it was included with.
"""

import argparse
import json
import logging
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

import toml
from packaging.requirements import SpecifierSet

from .models import PrivDep, process_toml_dict

logging.basicConfig(format="%(levelname)s\t: %(message)s")
log = logging.getLogger(__package__)
log.setLevel(logging.WARNING)

description = (
    "Pull private python (pip) requirements using fallback GitLab authententicaton."
)

epilog = "See DEPENDENCIES.md and the example in private-deps.toml for more detail."


def get_token(token_var):
    """Get the token from the environment or error."""
    if token_var in os.environ and len(os.environ[token_var]) > 0:
        return os.environ[token_var]
    log.warning(f"Environmental variable {token_var} is missing.")
    return None


def clone(
    name: str,
    gitlab_host: str,
    gitlab_path: str,
    gitlab_spec: str | None,
    token_var: str = "CI_JOB_TOKEN",
    **kwargs,
):
    """Try to clone this project, but not pip-install it."""


def installer(
    name: str,
    extras: list,
    dep: PrivDep,
):
    """Try to install this package, either in CI, or locally, or via SSH."""
    token_var = dep.token_var

    # We hit Kaniko only in the prebuild CI stage for caching our toolchain.
    # Kaniko cannot grab the env vars. Need to load from JSON.
    kaniko_file = Path("/kaniko/.docker/config.json")
    we_are_in_kaniko = False
    if kaniko_file.exists():
        we_are_in_kaniko = True
        log.warning("We are in a Kaniko build. Reloading env vars from JSON.")
        kaniko_config = json.load(kaniko_file.open())
        for varname in [
            "CI",
            "CI_JOB_NAME",
            "CI_JOB_STAGE",
            "CI_JOB_TOKEN",
            "CI_PROJECT_NAME",
            dep.token_var,
        ]:
            if varname in kaniko_config:
                os.environ[varname] = kaniko_config[varname]
                log.warning(f"Saving variable {varname} to env from kaniko")

    if "CI" in os.environ and os.environ["CI"] == "true":
        log.warning(
            f"We are in CI at stage {os.environ['CI_JOB_STAGE']} job {os.environ['CI_JOB_NAME']}"  # noqa: E501
        )
        # We hit Kaniko only in the prebuild CI stage for caching our toolchain.
        # So, this should be used ONLY IF always_pull is False
        if we_are_in_kaniko and dep.always_pull:
            # Abort early so we don't cache in kaniko build
            log.warning(
                f"Skipping {name} due to 'always_pull' option {dep.always_pull}"
            )
            return None
        token_var = "CI_JOB_TOKEN"

    token = get_token(token_var)
    extras_str = ""
    if extras is not None and len(extras) > 0:
        extras_str = "[" + ",".join(extras) + "]"

    path = Path(os.path.pardir, name)
    git = Path(path, ".git")

    # First, match the NON-PIP methods.
    match dep.method:
        case "docker":
            docker_tag = "latest"
            if dep.gitlab_spec and dep.gitlab_spec.startswith("v"):
                docker_tag = dep.gitlab_spec.replace(".", "-")
            total_cmd = [
                [
                    "docker",
                    "login",
                    f"{dep.gitlab_host}:5115",
                    "-u",
                    "git",
                    "-p",
                    f"${token_var}",
                ],
                [
                    "docker",
                    "pull",
                    f"{dep.gitlab_host}:5115/{dep.gitlab_path}:{docker_tag}",
                ],
                [
                    "docker",
                    "run",
                    "-p",
                    "8000:80",
                    f"{dep.gitlab_host}:5115/{dep.gitlab_path}:{docker_tag}",
                ],
            ]
            return total_cmd
        case "clone":
            cmd = ["git", "clone"]
            if dep.gitlab_spec:
                cmd.extend(["-b", dep.gitlab_spec])
            else:
                log.warning("No gitlab_spec provided. The default branch will be used.")
            if token:
                end_cmd = [
                    f"https://gitlab:${token_var}@{dep.gitlab_host}/{dep.gitlab_path}.git",
                    name,
                ]
            else:
                log.warning("Cloning via SSH. Hopefully your credentials work.")
                end_cmd = [f"git@{dep.gitlab_host}:{dep.gitlab_path}.git", name]
            return [cmd + end_cmd]
        case _:
            pass

    cmd = ["pip", "install"]
    if dep.always_pull:
        cmd.append("-U")  # force newest version, even if there was a cache
    if dep.no_deps:
        cmd.append("--no-deps")

    if dep.method == "local":
        log.warning(
            f"Using local clone at {path}. gitlab_spec and version_set ignored!"
        )
        if not (git.exists() and git.is_dir()):
            log.error(f"No local clone found at {path}.  Use --method 'clone' first?")
        end_cmd = ["-e", f"{path}"]
    elif dep.method == "wheel" and token:
        log.info("Pulling wheel from private registry index.")
        url_path = quote(
            dep.gitlab_path, safe=""
        )  # URLEncode the group and project name.
        end_cmd = [
            f"{name}{extras_str}{SpecifierSet(dep.version_set)}",
            "--index-url",
            f"https://gitlab-ci-token:${token_var}@{dep.gitlab_host}/api/v4/projects/{url_path}/packages/pypi/simple",
        ]
    elif dep.method == "source" and token:
        log.warning("Pulling source via direct HTTP install.")
        if not dep.gitlab_spec:
            gitlab_spec_str = ""
            log.warning("No gitlab_spec provided. The default branch will be used.")
        else:
            gitlab_spec_str = "@" + dep.gitlab_spec
        end_cmd = [
            f"{name}{extras_str}@git+https://gitlab-ci-token:${token_var}@{dep.gitlab_host}/{dep.gitlab_path}.git{gitlab_spec_str}"
        ]
    else:
        log.warning("Pulling source via SSH.  Hopefully your credentials work.")
        if not dep.gitlab_spec:
            gitlab_spec_str = ""
            log.warning("No gitlab_spec provided. The default branch will be used.")
        else:
            gitlab_spec_str = "@" + dep.gitlab_spec
        end_cmd = [
            f"{name}{extras_str}@git+ssh://git@{dep.gitlab_host}/{dep.gitlab_path}.git{gitlab_spec_str}"
        ]

    return [cmd + end_cmd]


# regex from PEP-345
# See https://packaging.python.org/en/latest/specifications/dependency-specifiers/#names
name_extras_re = re.compile(
    r"^(?P<name>[A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])($|\[(?P<extras>.*)\]$)",
    flags=re.IGNORECASE,
)


def main():
    """Run CLI."""
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--toml",
        type=str,
        default="private-deps.toml",
        help="Path to private deps TOML file.",
    )
    parser.add_argument(
        "-n",
        "--dry_run",
        action="store_true",
        help="Show a command, but do not run it.  See also --force",
    )
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        help="""Force a particular install method, overriding toml defaults.
        Options are 'docker', 'wheel', 'src', 'clone', 'local'.""",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase LogLevel verbosity, up to 3 times.",
    )

    args = parser.parse_args()

    assert args.verbose <= 2, "More than 2 `-v`'s is meaningless."
    log.setLevel(30 - 10 * args.verbose)

    log.info(f"Processing {args.toml}")
    # if args.method is not None:
    #    log.warning(f"Overriding methods with -m {args.method}")
    packages = process_toml_dict(toml.load(args.toml))
    for name, data in packages.items():
        if args.method is not None:
            log.warning(
                f"Overriding toml method='{data['dep'].method}' with -m {args.method}"
            )
        if args.method is not None:
            tmp_dep = data["dep"].model_dump()
            tmp_dep["method"] = args.method
            data["dep"] = PrivDep.model_validate(tmp_dep)

        total_cmd = installer(name, data["extras"], data["dep"])
        if total_cmd:
            log.info("Here is your command. You might need quotes.")
            for line in total_cmd:
                print(" ".join(line))
                # print(f"  $  {' '.join(line)}")
                if not args.dry_run:
                    subprocess.run(line, check=True)


if __name__ == "__main__":
    main()
