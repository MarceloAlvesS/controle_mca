from django.db.models import Model

def remove_object_model(model:Model, field:str, list_remove: list):
  for remove in list_remove:
    model.objects.filter(**{field:remove}).delete()