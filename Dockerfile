ARG PYTHON3_VERSION="3"

FROM python:${PYTHON3_VERSION}

WORKDIR /opt/hypothesis_sqlalchemy

COPY ./hypothesis_sqlalchemy hypothesis_sqlalchemy
COPY ./tests tests
COPY ./setup.py setup.py
COPY ./setup.cfg setup.cfg

RUN python3 -m pip install .
