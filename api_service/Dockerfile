FROM python:3.12
WORKDIR /api_service
COPY . .
RUN pip install flask flask_swagger_ui requests pytest grpcio grpcio-tools
CMD ["python", "api_service/api_service.py"]
