# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY . /code/

# install requirements 
RUN pip3 install -r requirements.txt

# install cron(for background process) and nano(for debugging through the files if needed)
RUN apt-get update && apt-get -y install cron && apt-get -y install nano

COPY fetch-data-crontab /etc/cron.d/fetch-data-crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/fetch-data-crontab

# Apply cron job
RUN crontab /etc/cron.d/fetch-data-crontab
 
# Create the log file to be able to tail
RUN touch /var/log/cron.log
 
