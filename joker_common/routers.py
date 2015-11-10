class AuthRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "joker_model_1" or model._meta.app_label == "joker_model_2" or model._meta.app_label == "joker_model_4":
            return "smartcube_models"
        else:
            return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "joker_model_1" or model._meta.app_label == "joker_model_2" or model._meta.app_label == "joker_model_4":
            return "smartcube_models"
        else:
            return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == "joker_model_1" or app_label == "joker_model_2" or app_label == "joker_model_4":
            return db == "smartcube_models"
        return None
