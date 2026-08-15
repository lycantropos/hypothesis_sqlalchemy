ARG IMAGE_NAME
ARG IMAGE_VERSION

FROM ${IMAGE_NAME}:${IMAGE_VERSION}

WORKDIR /opt/hypothesis_sqlalchemy

COPY pyproject.toml .
COPY README.md .
COPY setup.py .
COPY hypothesis_sqlalchemy hypothesis_sqlalchemy
COPY tests tests

RUN pip install -e .[tests]
