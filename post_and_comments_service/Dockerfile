FROM python:3.12
WORKDIR /post_and_comments_service
COPY . .
RUN pip install flask psycopg2 dotenv flask_swagger_ui requests pytest pytest-grpc grpcio grpcio-tools
CMD ["python", "post_and_comments_service.py"]
