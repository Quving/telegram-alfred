FROM python:3.6

WORKDIR /workdir

ADD . .
RUN pip install -r requirements.txt

CMD ["python", "run.py"]



