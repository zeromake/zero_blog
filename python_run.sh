#!/bin/sh
sudo docker run --name blog_run -v ${PWD}/blog:/blog -p 8096:8000 zeromake/blog python /blog/main.py
