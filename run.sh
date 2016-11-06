#!/bin/sh
sudo docker run -v ${PWD}/blog:/blog -p 80:80 -d zeromake/blog-docker
