#!/bin/sh
sudo docker run --name blog -v ${PWD}/blog:/blog -p 8096:80 zeromake/blog
