#!/bin/sh
sudo nginx -s stop
killall gunicorn
gunicorn --limit-request-line 8190 -b unix:`pwd`/run/gunicorn.sock api.wsgi:application &
nginx -c `pwd`/nginx/nginx.conf
