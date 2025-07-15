FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY docker_requirements.txt .

RUN pip install --no-cache-dir -r docker_requirements.txt

COPY src/ src/
COPY scripts/ scripts/
COPY config/ config/
COPY analytics_api/ analytics_api/

COPY .env .env

CMD ["python", "-c", "print('Docker container ready for action ✅')"]