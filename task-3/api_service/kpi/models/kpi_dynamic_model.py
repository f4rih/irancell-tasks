from django.db import models
from django.apps import apps


def kpi_dynamic_model(table_name):
    """
    Create a dynamic model for the given kpi name.
    """
    if apps.is_installed(table_name):
        return apps.get_model(table_name)

    class Meta:
        managed = False
        db_table = table_name

    attrs = {
        "__module__": __name__,
        "Meta": Meta,
        "field_type": models.CharField(max_length=50),
        "field_name": models.CharField(max_length=255),
        "value": models.DecimalField(max_digits=20, decimal_places=8),
        "agg_type": models.CharField(max_length=10),
    }
    return type(table_name, (models.Model,), attrs)