#!/bin/sh
sudo docker run -v ${PWD}/blog:/blog -p 8096:80 -d zeromake/blog-docker
