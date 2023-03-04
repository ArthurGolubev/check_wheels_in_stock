FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes






FROM python:3.10

WORKDIR /cwis

COPY --from=requirements-stage /tmp/requirements.txt /cwis/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /cwis/requirements.txt

COPY ./parser .

ENTRYPOINT [ "python3", "Parser.py"]
