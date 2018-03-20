FROM nginx:1.9

#  default conf for proxy service
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# NOT FOUND response
COPY ./backend-not-found.html /var/www/html/backend-not-found.html

#  Proxy and SSL configurations
COPY ./includes/ /etc/nginx/includes/
