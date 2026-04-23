FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser
USER appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK CMD python -c "import sys; sys.exit(0)"

CMD ["python", "worker.py"]