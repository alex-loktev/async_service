FROM python:3.7-slim


WORKDIR /home/code/worker
RUN pip install --upgrade pip
COPY requirements.txt /home/code/worker/requirements.txt
RUN pip install -r requirements.txt

COPY . /home/code/worker

CMD ["python3.7", "worker.py"]

EXPOSE 8081/tcp