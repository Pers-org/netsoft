# Example

# FROM ubuntu:22.04 AS builder

# ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get install -y \
#     python3.11 python3-pip libpq-dev python3.11-dev \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt . 
# RUN python3.11 -m pip wheel -r requirements.txt -w /wheels


FROM python:3.11-slim

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY ./app/API.py .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8000"]

