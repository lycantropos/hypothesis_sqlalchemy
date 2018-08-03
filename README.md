`hypothesis` strategies for `SQLAlchemy`
========================================

[![](https://travis-ci.org/lycantropos/hypothesis_sqlalchemy.svg?branch=master)](https://travis-ci.org/lycantropos/hypothesis_sqlalchemy "Travis CI")
[![](https://ci.appveyor.com/api/projects/status/6a33c5sfm4gy0iup/branch/master?svg=true)](https://ci.appveyor.com/project/lycantropos/hypothesis-sqlalchemy/branch/master "AppVeyor")
[![](https://ci.appveyor.com/api/projects/status/3ivakruo0f156yrp?svg=true)](https://ci.appveyor.com/project/lycantropos/monty "AppVeyor")
[![](https://codecov.io/gh/lycantropos/hypothesis_sqlalchemy/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/hypothesis_sqlalchemy "Codecov")
[![](https://img.shields.io/github/license/lycantropos/monty.svg)](https://github.com/lycantropos/hypothesis_sqlalchemy/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/hypothesis_sqlalchemy.svg)](https://badge.fury.io/py/hypothesis_sqlalchemy "PyPI")

In what follows `python3` is an alias for `python3.5` or any later
version (`python3.6` and so on).

Installation
============

Install the latest `pip` & `setuptools` packages versions

```bash
python3 -m pip install --upgrade pip setuptools
```

Release
-------

Download and install the latest stable version from `PyPI` repository

```bash
python3 -m pip install --upgrade hypothesis_sqlalchemy
```

Developer
---------

Download and install the latest version from `GitHub` repository

```bash
git clone https://github.com/lycantropos/hypothesis_sqlalchemy.git
cd hypothesis_sqlalchemy
python3 setup.py install
```

Running tests
=============

Plain

```bash
python3 setup.py test
```

Inside `Docker` container

```bash
docker-compose up
```
