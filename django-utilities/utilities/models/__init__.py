from django.db import models

def encode(model):
	return '%s.%s' % (model._meta.app_label, model._meta.object_name.lower())

def decode(string):
	return models.get_model(*string.split('.'))
