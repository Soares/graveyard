from django.db import models


class Tag(models.Model):
	name = models.SlugField(primary_key=True)


class Entry(models.Model):
	slug = models.SlugField(primary_key=True)
	name = models.CharField(max_length=100)
	text = models.TextField()
	tags = models.ManyToManyField(Tag)
	created = models.DateField(auto_now_add=True)
	published = models.DateField(blank=True, null=True)
	updated = models.DateField(auto_now=True)
