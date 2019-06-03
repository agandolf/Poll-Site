FROM python:latest
MAINTAINER Austin Gandolfi "agandolf@umich.edu"

RUN apt-get update -y
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN chmod g+r -R ./polls
RUN chmod 1777 /tmp
RUN chmod g+rw ./db.sqlite3

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]