FROM python:latest
MAINTAINER Austin Gandolfi "agandolf@umich.edu"

RUN apt-get update -y
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["py", "manage.py", "runserver"]
