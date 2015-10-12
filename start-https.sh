#!/bin/sh
sudo nginx -s stop
killall gunicorn
gunicorn --limit-request-line 8190 -t 1800 -b 127.0.0.1:9000 joker.wsgi:application &
sudo nginx -c `pwd`/nginx/nginx.conf
