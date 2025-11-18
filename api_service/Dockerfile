FROM python:3.12
WORKDIR /api_service
COPY . .
RUN pip install protobuf==5.29.0 grpcio==1.71.0 grpcio-tools==1.71.0 flask flask_swagger_ui requests pytest
CMD ["python", "api_service/api_service.py"]
