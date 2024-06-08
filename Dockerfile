FROM python:3.10-bullseye
RUN apt-get update -y && mkdir /app
RUN apt-get install build-essential cmake python3-dev -y
COPY . /app
WORKDIR /app
ARG LOGFIRE_API_KEY 
ARG OPENAI_API_KEY
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main
EXPOSE 8080
ENTRYPOINT [ "sh", "-c", "cd .. && writer run app --port 8080 --host 0.0.0.0" ]