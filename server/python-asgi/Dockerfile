FROM python:3.9
ADD requirements.txt /app/requirements.txt
ADD test.env /app/.env
ADD pk.json /app/pk.json
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "main:asgi_app", "--host", "0.0.0.0", "--port", "8080", "--app-dir", "."]