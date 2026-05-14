FROM python:3.12-slim
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends awscli && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python3", "application.py"]