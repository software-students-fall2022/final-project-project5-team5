FROM python:3.9.2

ADD app.py .

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

CMD [ "python3", "./app.py" ]