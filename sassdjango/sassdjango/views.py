import os
from django.http import HttpResponse
from django import conf
from mangaement.commands.sass2css import Command as Convert
from management.commands.procss import Command as Process

def sass(request, filename):
	convert = Convert().convert
	process = Process().process
	base = conf.settings.get('SASS_DIR')
	with open(os.path.join(base, filename)) as file:
		output = process(convert(file.read())) 
	return HttpResponse(output, mimetype='text/css')
