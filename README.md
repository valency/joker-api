# Project Joker: API Layer

```
python manage.py migrate --database=auth_db
python manage.py migrate
```

The following settings of API server may need to be changed:
- `SQLITE_DIR` (`/data/var/`) and `DATABASES` in `joker/settings.py`
- `DATA_PATH` in `joker_common/views.py`

The following settings of UI server may need to be changed:
- `API_PORT`, `API_PROTOCOL` in `js/common.js`
