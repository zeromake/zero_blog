#!/bin/sh
sudo docker run -v ${PWD}/blog:/blog -p 8096:8000 zeromake/blog-docker python /blog/main.py