FROM node:10.2.1

RUN mkdir -p /lxn/backend
ADD . /lxn/backend
WORKDIR /lxn/backend
EXPOSE 5000

CMD ["sh", "./start.sh"]