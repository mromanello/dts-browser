FROM python:3.9-alpine as python

ENV AGGREGATOR_URL='http://localhost:5051'
ENV PORT=5051

RUN mkdir /root/DTS-browse
WORKDIR /root/DTS-browser

COPY ["./", "./"]

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "launcher.py"]