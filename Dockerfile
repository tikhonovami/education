FROM python:3.10-buster
RUN mkdir /education
WORKDIR /education
COPY poetry.lock pyproject.toml /education
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install
COPY . .
CMD ["./.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]