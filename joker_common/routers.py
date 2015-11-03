class AuthRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "joker_auth":
            return "auth_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "joker_auth":
            return "auth_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "joker_auth" or obj2._meta.app_label == "joker_auth":
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == "joker_auth":
            return db == "auth_db"
        return None
