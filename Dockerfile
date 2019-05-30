FROM python:3.7
MAINTAINER Austin Gandolfi "agandolf@umich.edu"
RUN apt-get update -y

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000
COPY . .
CMD ["py", "manage.py", "runserver"]
