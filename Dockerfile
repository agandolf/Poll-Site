FROM python:latest
MAINTAINER Austin Gandolfi "agandolf@umich.edu"

RUN apt-get update -y
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN chmod g+rw -R .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]