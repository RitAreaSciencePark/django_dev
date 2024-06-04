class ExternalDbRouter:


    route_app_labels = {"external_db_app"}

    # -- Normal routing operations
    def db_for_read(self, model, **hints):
        # Attempts to read models go to external_generic_db.
        if model._meta.app_label in self.route_app_labels:
            return 'external_generic_db'
        return None

    def db_for_write(self, model, **hints):
        # Attempts to write models go to external_generic_db.
        if model._meta.app_label in self.route_app_labels:
            return 'external_generic_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if a model in the external_db_app is involved.
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    # -- this takes effect only on migration (migrate)
    # REMEMBER: WHEN MIGRATE use python3 manage.py migrate && python3 manage.py migrate --database=external_generic_db
    # TO MIGRATE BOTH DATABASES! THIS IS MANDATORY TO POPULATE THE external_generic_db
    def allow_migrate(self, db, app_label, model_name=None, **hints):

        # Make sure the external_db_app creates only tables defined into the model (and django_migrations)
        # And viceversa, in the default db there are only webapp related tables

        if db == 'external_generic_db':
            if app_label in self.route_app_labels:
                return True # Everything that is external_db_app will be included in external_generic_db
            else:
                return False # Everything that is not external_db_app will be excluded in external_generic_db (no useless table replication)
        else:
            if app_label in self.route_app_labels:
                return False # Do not include external_db_app models
            else:
                return None # Everything that is not external_db_app will be deferred to the default db
                