FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y git

WORKDIR /bot
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "__main__.py"]