FROM python:3

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app


ENTRYPOINT ["python"]

CMD ["app.py"]
