#!/bin/sh
git_href=https://github.com/zeromake/zeromake.github.io.git


sudo docker run -v ${PWD}/blog:/blog zeromake/blog-docker python /blog/main.py make &&\
 sudo chown $USER:$USER ${PWD}/blog/build -R

if [ ! -x "static_blog" ]; then
	git clone $git_href static_blog && cd static_blog
else
	cd static_blog && git pull
fi

rm -rf ./index.html ./pages ./static

cp -R ../blog/build/* ./

git add ./

git commit -m "bash auto commit on `date '+%Y-%m-%d %H:%M:%S'`" && git push
