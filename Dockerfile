FROM python:3.10-slim

WORKDIR /proyecto

COPY ./requirements.txt /proyecto/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /proyecto/requirements.txt

COPY ./app /proyecto/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]