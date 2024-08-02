class HistoryRouter:
    history_models = {'userhistory', 'uploadhistory', 'downloadhistory'}

    def db_for_read(self, model, **hints):
        if model._meta.model_name.lower() in self.history_models:
            print(f"Routing {model._meta.model_name} to 'history' database for read.")
            return 'history'
        print(f"Routing {model._meta.model_name} to 'default' database for read.")
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.model_name.lower() in self.history_models:
            print(f"Routing {model._meta.model_name} to 'history' database for write.")
            return 'history'
        print(f"Routing {model._meta.model_name} to 'default' database for write.")
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.model_name.lower() in self.history_models or
            obj2._meta.model_name.lower() in self.history_models
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name and model_name.lower() in self.history_models:
            print(f"Routing {model_name} to 'history' database for migration.")
            return db == 'history'
        print(f"Routing {model_name} to 'default' database for migration.")
        return db == 'default'