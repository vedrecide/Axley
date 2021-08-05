FROM python:3.9-slim
WORKDIR /bot
COPY . .
RUN pip install -r ./axley/requirements.txt
CMD ["python3", "-m", "axley"]

# docker-compose up -d --build