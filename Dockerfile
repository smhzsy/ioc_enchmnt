FROM python:latest

WORKDIR /app


COPY . .


RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root


CMD ["python", "api.py"]
