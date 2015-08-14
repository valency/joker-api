#!/bin/sh
sudo nginx -s stop
killall gunicorn
gunicorn --limit-request-line 8190 -t 1800 -b unix:`pwd`/run/gunicorn.sock joker.wsgi:application &
nginx -c `pwd`/nginx/nginx.conf
