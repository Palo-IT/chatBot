FROM ubuntu:16.04
MAINTAINER aloustaunau@palo-it.com 

RUN apt-get update
RUN apt-get install -y curl nginx python-pip supervisor

RUN pip install gunicorn Flask pyee slackclient mysql_connector pandas

#enable supervisor.conf
#serveur web HTTP WSGI
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

EXPOSE 3001
CMD ["/usr/bin/supervisord", "-n"]
