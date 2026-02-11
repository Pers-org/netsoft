FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-flask \
    py3-fastapi

COPY app.py .

CMD ["python", "app.py"]
