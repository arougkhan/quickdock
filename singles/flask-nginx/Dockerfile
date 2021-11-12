FROM python:3.8-buster

# Install nginx
COPY ./config/nginx/install-nginx-debian.sh /
RUN bash /install-nginx-debian.sh
EXPOSE 80
EXPOSE 443
ENV LISTEN_PORT 80

# Install requirements ??
#COPY requirements.txt /tmp/requirements.txt
#RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Remove default configuration from nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY ./config/uwsgi/uwsgi.ini /etc/uwsgi/

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*
COPY ./config/supervisor/supervisord-debian.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./config/supervisor/stop-supervisor.sh /etc/supervisor/stop-supervisor.sh
RUN chmod +x /etc/supervisor/stop-supervisor.sh

# uWSGI Python plugin
ENV UWSGI_INI /app/uwsgi.ini
ENV UWSGI_CHEAPER 2
ENV UWSGI_PROCESSES 16
# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0
ENV NGINX_WORKER_PROCESSES 1

# Configure start script and entrypoint
COPY ./config/start.sh /start.sh
COPY ./config/uwsgi/uwsgi-nginx-entrypoint.sh /uwsgi-nginx-entrypoint.sh
COPY ./config/entrypoint.sh /entrypoint.sh
RUN chmod +x /start.sh
RUN chmod +x /uwsgi-nginx-entrypoint.sh
RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["sh", "/uwsgi-nginx-entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]

# Install requirements
COPY ./config/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# URL from which static files will be requested (bypasses uWSGI)
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

# Add Python application files
COPY ./src /app
WORKDIR /app
ENV PYTHONPATH=/app

# Run the start script provided by the parent image tiangolo/uwsgi-nginx.
# It will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/start.sh"]

###########################################################################
# Based on docker sample uWSGI by Sebastian Ramirez <tiangolo@gmail.com>" #
###########################################################################
