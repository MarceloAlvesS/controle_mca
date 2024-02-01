from django.db.models import Model

def model_register(model: Model, **kwargs):
    request = model.objects.filter(**kwargs).first()
    if request:
        return request
    else:
        return model.objects.create(**kwargs)