# use Docker's provided python image
FROM python:2.7
MAINTAINER natebrennand <natebrennand@gmail.com>

RUN apt-get update -y
RUN apt-get install rubygems -y
RUN gem install sass

# install all packages
COPY ./config/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add the application directories
ADD ./ /
WORKDIR /

# expose the port and start the server
EXPOSE 6000
CMD gunicorn deploy:app -b 0.0.0.0:6000 --log-file /opt/logs/gunicorn.log --log-level debug
