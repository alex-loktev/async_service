FROM python:3.7-slim

WORKDIR /home/code/web
RUN pip install --upgrade pip
COPY requirements.txt /home/code/web/requirements.txt
RUN pip install -r requirements.txt

COPY . /home/code/web

CMD ["python3.7", "main.py"]

