ARG IMAGE_NAME
ARG IMAGE_VERSION

FROM ${IMAGE_NAME}:${IMAGE_VERSION}

RUN pip install --upgrade pip setuptools

WORKDIR /opt/hypothesis_sqlalchemy

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY requirements-tests.txt .
RUN pip install -r requirements-tests.txt

COPY README.md .
COPY pytest.ini .
COPY setup.py .
COPY hypothesis_sqlalchemy hypothesis_sqlalchemy
COPY tests tests
