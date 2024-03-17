FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python3 -m venv venv
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]