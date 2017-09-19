FROM python:3.5

WORKDIR /opt/hypothesis_sqlalchemy
COPY . /opt/hypothesis_sqlalchemy/
RUN python3 -m pip install .
