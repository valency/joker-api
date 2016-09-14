# Installation Guide
## Install Compulsory Packages
```
apt install git vim screen php-curl php-fpm postgresql postgresql-contrib nginx python-pip python-psycopg2 python-pandas python-numpy python-scipy
pip install Django djangorestframework django-filter django-cors-headers django-queryset-csv xlsxwriter
```
## Configure PostgreSQL
```
sudo vim /etc/postgresql/9.5/main/pg_hba.conf
```
Modify the authentication of all connections to `trust`.
```
sudo /etc/init.d/postgresql restart
```
## Configure NGINX
```
sudo vim /etc/nginx/sites-available/default
```
Add the following settings to `server` section:
```
location /api/joker/ {
    proxy_pass http://127.0.0.1:9002/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 43200000;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
    proxy_set_header X-NginX-Proxy true;
    proxy_buffering off;
}
```
```
sudo service nginx restart
```
## Set Up the System
```
psql -h localhost -U postgres postgres -c "CREATE DATABASE smartcube;"
python manage.py migrate
python manage.py migrate --database=joker_models
python manage.py collectstatic
mv static /var/www/html/
python manage.py runserver 0.0.0.0:9002
```
# Frequently Asked Questions
## The following settings of API server may need to be changed:
- `SQLITE_DIR` (`/data/var/`) in `joker/settings.py`
- `USER` (`smartcube`) under `DATABASES` in `joker/settings.py`
- `DATA_PATH` (`/home/smartcube/local/...`) in `joker_common/views.py`

##The following settings of UI server may need to be changed:
- `API_PORT` (`443`), `API_PROTOCOL` (`https`) in `js/conf.js`
- `$DOMAIN` (`127.0.0.1:8080`) in `components/common.php`
- `chmod a+w` for `data`, `validation`, and `validation/ground-truth`
