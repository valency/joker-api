from django.conf import settings


def interpret_db_by_app(app):
    if app in settings.DATABASES["joker_models"]["APPS"]:
        return "joker_models"
    elif app in settings.DATABASES["joker_summary"]["APPS"]:
        return "joker_summary"
    else:
        return None


class AuthRouter(object):
    def db_for_read(self, model, **hints):
        return interpret_db_by_app(model._meta.app_label)

    def db_for_write(self, model, **hints):
        return interpret_db_by_app(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        target_db = interpret_db_by_app(app_label)
        if target_db is None:
            return None
        else:
            return db == target_db
