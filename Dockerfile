ARG PYTHON_IMAGE
ARG PYTHON_IMAGE_VERSION

FROM ${PYTHON_IMAGE}:${PYTHON_IMAGE_VERSION}

RUN pip install --upgrade pip setuptools

WORKDIR /opt/hypothesis_sqlalchemy

COPY requirements.txt .
RUN pip install --force-reinstall -r requirements.txt

COPY requirements-tests.txt .
RUN pip install --force-reinstall -r requirements-tests.txt

COPY README.md .
COPY pytest.ini .
COPY setup.py .
COPY hypothesis_sqlalchemy hypothesis_sqlalchemy/
COPY tests/ tests/
