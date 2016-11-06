FROM alpine:latest

MAINTAINER zeromake <a390720046@gmail.com>

COPY ./blog/requirements.txt /tmp/requirements.txt

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories &&\
 	apk --update add python python-dev py-pip nginx gcc g++ make linux-headers &&\
 	pip install -r /tmp/requirements.txt

COPY conf/nginx.conf  /etc/nginx/nginx.conf
COPY conf/uwsgi.ini /etc/uwsgi/
COPY conf/supervisord.conf /etc/supervisor/supervisord.conf

WORKDIR /blog
EXPOSE 80 443

CMD ["supervisord"]
