FROM python:3.8

RUN pip install --upgrade pip

RUN pip install torchaudio omegaconf pika pyftpdlib numpy

COPY src/ .

RUN mkdir results

CMD [ "python", "./main.py" ] 