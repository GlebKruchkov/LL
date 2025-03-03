FROM python:3.12
WORKDIR /api_service
COPY . .
RUN pip install flask flask_swagger_ui requests
CMD ["python", "api_service.py"]
