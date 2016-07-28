To set up the system:
```
psql -h localhost -U postgres postgres -c "CREATE DATABASE smartcube;"
python manage.py migrate
python manage.py migrate --database=smartcube_models
python manage.py createsuperuser
python manage.py collectstatic
mv static /var/www/html/
python manage.py runserver 0.0.0.0:9002
```

The following settings of API server may need to be changed:
- `SQLITE_DIR` (`/data/var/`) in `joker/settings.py`
- `USER` (`smartcube`) under `DATABASES` in `joker/settings.py`
- `DATA_PATH` (`/home/smartcube/local/...`) in `joker_common/views.py`

The following settings of UI server may need to be changed:
- `API_PORT` (`443`), `API_PROTOCOL` (`https`) in `js/conf.js`
- `$DOMAIN` (`127.0.0.1:8080`) in `components/common.php`
- `chmod a+w` for `data`, `validation`, and `validation/ground-truth`
