FROM python:3.6
ADD . /agenda
WORKDIR /agenda
COPY . .
RUN pip install Flask
RUN pip install flask_wtf
RUN pip install wtForms
RUN pip install email_validator
RUN pip install flask_bcrypt
RUN pip install flask_login
RUN pip install flask_SQLAlchemy
CMD [ "python", "./app.py" ]
EXPOSE 5000