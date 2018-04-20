FROM ubuntu:16.04
MAINTAINER aloustaunau@palo-it.com

RUN apt-get update \
   && apt-get install -y software-properties-common python3-dev \
   && add-apt-repository ppa:jonathonf/python-3.6\
   && apt-get update 
RUN apt-get install -y curl python3.6 nginx supervisor python3-pip locales tzdata


RUN python3.6 -m pip install gunicorn Flask pyee slackclient mysql_connector pandas

RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

#enable supervisor.conf
#serveur web HTTP WSGI
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

CMD ["/usr/bin/supervisord", "-n"]
