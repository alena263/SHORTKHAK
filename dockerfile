FROM python:3.14-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    python -m pip install PyQt5

CMD ["python", "TRY.py"]
