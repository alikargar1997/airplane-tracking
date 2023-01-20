FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip

RUN apt-get clean && apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y --no-install-recommends gcc libpq-dev libc-dev python3-dev gettext binutils
RUN rm -rf /var/lib/apt/lists/*



WORKDIR /app/
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
