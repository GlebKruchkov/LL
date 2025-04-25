FROM python:3.12
WORKDIR /post_and_comments_service
COPY . .
RUN pip install protobuf==5.29.0 grpcio==1.71.0 grpcio-tools==1.71.0 flask psycopg2 dotenv flask_swagger_ui requests pytest pytest-grpc kafka-python
CMD ["python", "post_and_comments_service.py"]
