# OSSWiz - the Wizard of OSS

## Usage

You can run osswiz checks (through [repo-review](https://repo-review.readthedocs.io/en/latest/)) from the command line to interactively check your project:

```console
# If you have the package installed
$ osswiz

# If you don't have the package installed
$ pipx run --spec git+https://github.com/AdrianoKF/osswiz@main osswiz
# or, using uv:
$ uvx --from git+https://github.com/AdrianoKF/osswiz osswiz
```

If want to run checks automatically whenever you make a commit, you can use the osswiz [`pre-commit`](https://pre-commit.com) hook:

```yaml
- repo: https://github.com/AdrianoKF/osswiz
  rev: main # or desired version from releases/tags
  hooks:
    - id: osswiz
```

## License

This project is licensed under the terms of the Apache-2.0 license.
