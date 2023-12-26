FROM python:3.9-alpine
WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install --root-user-action=ignore --no-cache-dir --upgrade -r /app/requirements.txt
COPY docker-start.sh /app/docker-start.sh