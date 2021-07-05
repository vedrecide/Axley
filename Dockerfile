FROM python:3.9-slim
WORKDIR /bot
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "__main__.py"]
# docker-compose up -d --build