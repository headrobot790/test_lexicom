FROM python:3.11-slim
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
