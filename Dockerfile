FROM python:3.10-slim-buster 
ADD . /Agenda
WORKDIR /Agenda
COPY . .
RUN pip install flask 
CMD [ "python", "app.py" ]
EXPOSE 5000