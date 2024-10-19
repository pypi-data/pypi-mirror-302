# Briton

The python side of Briton. Briton server is written in C++ for high performance
and provides a grpc endpoint for interaction. A major function of this python
libarary is to provide easier interaction with the Briton Server. e.g. there's
logic to startup the Briton server and ensure it's healthy. It also provides
adapters for using Briton from Truss. For certain features, such as draft model
based speculative decoding, a subtantial chunk of the implementation is in this
library.

## Running tests

```
poetry run pytest
```

## Formatting code

```
poetry run ./format.sh
```

## Manually publishing to PyPi

Before running this, please increment the version appropriately in pyproject.toml.

Find the `basetenbot` credentials in 1Password, which can be used to sign into PyPi
and generate a token. This token can be saved in your `.pypirc` as follow:

```
[distutils]
  index-servers =
    pypi

[pypi]
  username = __token__
  password = # either a user-scoped token or a project-scoped token you want to set as the default
```

Or entered into the CLI when prompted by `twine upload` below:

```
rm -rf dist
poetry build
poetry run twine upload dist/*
```
