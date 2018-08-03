`hypothesis` strategies for `SQLAlchemy`
========================================

[![](https://travis-ci.org/lycantropos/hypothesis_sqlalchemy.svg?branch=master)](https://travis-ci.org/lycantropos/hypothesis_sqlalchemy "Travis CI")
[![](https://ci.appveyor.com/api/projects/status/6a33c5sfm4gy0iup/branch/master?svg=true)](https://ci.appveyor.com/project/lycantropos/hypothesis-sqlalchemy/branch/master "AppVeyor")
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

Usage
=====

Let's take a look at what can be generated and how.

Tables
------

Suppose we have metadata
```pydocstring
>>> from sqlalchemy.schema import MetaData 
>>> metadata = MetaData()
```

We can write a strategy that produces tables associated with given metadata
```pydocstring
>>> from hypothesis import strategies
>>> from hypothesis_sqlalchemy import tables
>>> tables_strategy = tables.factory(metadatas=strategies.just(metadata))
>>> table = tables_strategy.example()
>>> table.name
kahtvedrpis
>>> table.columns
['kahtvedrpis.wkeggvqvekovyornpixczunhlslpirtqbnpwdppjvccgvy', 
 'kahtvedrpis.olyrajvsfxbgxzmxheaxdwzgcaj']
```

Records
-------

Suppose we have a table
```pydocstring
>>> from sqlalchemy.schema import (Column,
                                   MetaData,
                                   Table)
>>> from sqlalchemy.sql.sqltypes import (Integer,
                                         String)
>>> metadata = MetaData()
>>> user_table = Table('user', metadata,
                       Column('user_id', Integer,
                              primary_key=True),
                       Column('user_name', String(16),
                              nullable=False),
                       Column('email_address', String(60)),
                       Column('password', String(20),
                              nullable=False))
```
and we can write strategy that
* produces single records (as `tuple`s)
    ```pydocstring
    >>> from hypothesis_sqlalchemy import tables
    >>> records = tables.records.factory(user_table)
    >>> records.example()
    (1022, '>5', None, '+b8a*,\x04&3<')
    ```
* produces records `list`s (with configurable `list` size bounds)
    ```pydocstring
    >>> from hypothesis_sqlalchemy import tables
    >>> records_lists = tables.records.lists_factory(user_table,
                                                     min_size=2,
                                                     max_size=5)
    >>> records_lists.example()
    [(11310, '', 'P\x02LT/Q\\', ''),
     (16747, '\x08*Z#j0 ;', None, ''),
     (29983, '', None, ''), 
     (7597, '', '}\x16', '<:+n$W')]
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
