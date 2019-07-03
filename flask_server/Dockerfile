FROM lesha1337/videorender

RUN pip install flask_cors requests

RUN mkdir -p /lxn/data
ADD . /lxn/flask_server
WORKDIR /lxn/flask_server
EXPOSE 10228

CMD ["python", "-u", "main.py"]