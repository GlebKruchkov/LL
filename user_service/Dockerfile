FROM python:3.12
WORKDIR /user_service
COPY . .
RUN pip install flask psycopg2 dotenv
CMD ["python", "user_service.py"]
