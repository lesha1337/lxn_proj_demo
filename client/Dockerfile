FROM node:10.2.1

RUN mkdir -p /lxn/client
ADD . /lxn/client
WORKDIR /lxn/client
EXPOSE 3000

CMD ["sh", "./start.sh"]