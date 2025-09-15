FROM python:3.12-slim

WORKDIR /app

ENV UV_LINK_MODE=copy

RUN pip install uv
COPY src ./src
COPY manage.py pyproject.toml uv.lock .
RUN uv venv

CMD ["uv", "run", "python", "-m", "gunicorn", "holiday_planner.asgi:application", "-k", "uvicorn_worker.UvicornWorker", "--bind", "0.0.0.0:8000"]