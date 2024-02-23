FROM python:3.11-slim
WORKDIR /app
COPY ./app /app
RUN pip install --no-cache-dir  -r requirements.txt
EXPOSE 8888
CMD ["python", "main.py"]