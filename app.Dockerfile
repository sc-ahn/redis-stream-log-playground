FROM python:3.10.4-bullseye

ENV POETRY_VERSION=1.4.0 POETRY_HOME=/poetry
ENV PATH=/poetry/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /huray/app
COPY pyproject.toml poetry.lock ./
COPY README.md ./
RUN poetry install --only main
COPY app app
COPY templates templates
COPY bin/app-start bin/start
CMD bin/start
