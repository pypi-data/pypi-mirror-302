# anaconda-cloud-cli

**DEPRECATED**

This package is now deprecated in favor of `anaconda-cli-base`, for which
anaconda-client 1.13 is a plugin.

The current version of `anaconda-cloud-cli` has no dependencies and does not
install modules to allow clean upgrades in pre-existing environments.

## Old description

The base CLI for Anaconda Cloud.
It currently provides the handling of cloud login/logout, and backwards-compatible passthrough of arguments to the core `anaconda-client` CLI.

This CLI is intended to provide identical behavior to `anaconda-client`, except for minor changes to the login/logout flow, to provide a gentle deprecation path.

## Setup for development

Ensure you have `conda` installed.
Then run:
```shell
make setup
```

## Run the unit tests
```shell
make test
```

## Run the unit tests across isolated environments with tox
```shell
make tox
```
