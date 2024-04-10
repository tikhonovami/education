FROM python:3.10-buster
RUN mkdir /education
WORKDIR /education
COPY poetry.lock pyproject.toml /education
RUN pip install --upgrade poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install
COPY . .
EXPOSE 8000
CMD ["./.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]