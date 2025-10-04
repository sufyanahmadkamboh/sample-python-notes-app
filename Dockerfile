# Simple production container
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Create DB at build time is optional; app creates on first run.
EXPOSE 5000
#CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

