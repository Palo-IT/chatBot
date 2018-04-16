FROM ubuntu:16.04
MAINTAINER aloustaunau@palo-it.com

RUN apt-get update \
   && apt-get install -y software-properties-common python3-dev \
   && add-apt-repository ppa:jonathonf/python-3.6\
   && apt-get update 
RUN apt-get install -y curl nginx python3-pip supervisor python3.6

RUN pip3 install gunicorn Flask pyee slackclient mysql_connector pandas

#enable supervisor.conf
#serveur web HTTP WSGI
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

CMD ["/usr/bin/supervisord", "-n"]