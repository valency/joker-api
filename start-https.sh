#!/bin/sh
killall gunicorn
gunicorn -b unix:`pwd`/run/gunicorn.sock api.wsgi:application &
nginx -c `pwd`/nginx/nginx.conf
