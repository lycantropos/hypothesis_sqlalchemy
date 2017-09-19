.. contents::


In what follows ``python3`` is an alias for ``python3.5``
or any later version (``python3.6`` and so on).

Installation
------------
Install the latest ``pip`` & ``setuptools`` packages versions

.. code-block:: bash

  python3 -m pip install --upgrade pip setuptools

Release
~~~~~~~
Download and install the latest stable version

.. code-block:: bash

  python3 -m pip install --upgrade hypothesis_sqlalchemy

Developer
~~~~~~~~~
.. code-block:: bash

  git clone https://github.com/lycantropos/hypothesis_sqlalchemy.git
  cd hypothesis_sqlalchemy
  python3 setup.py install

Running tests
-------------
Plain
.. code-block:: bash

    python3 setup.py test

Inside ``Docker`` container with remote debugger
.. code-block:: bash

    ./set-dockerhost.sh docker-compose up
