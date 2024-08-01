FROM python:3.10.14-slim

RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

RUN mkdir -p models
COPY "predict.py" "./"
COPY "models/model_C=1.0.bin" "./models/"
COPY "templates" "./templates/"
COPY "schema.yaml" "./"

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]   