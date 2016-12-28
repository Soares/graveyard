import re

def default(match):
	rule = match.group()
	for prefix in ('', '-moz-', '-webkit-'):
		yield prefix + rule

def corner(match):
	rule = match.group()
	p, tl, br, s, v = match.groups()
	yield rule
	yield '-webkit-' + rule
	yield '-moz-border-radius-%s%s:%s%s;' % (tl, br, s, v)

def opacity(match):
	rule = match.group()
	p, pad, value = match.groups()
	yield rule
	if re.match(r'^\s*\d+(\.\d+)?\s*$', value):
		yield 'filter:%salpha(opacity=%d);' % (pad, int(float(value) * 100));

processors = {
	r'box-sizing': default,
	r'border-radius': default,
	r'border-(top|bottom)-(right|left)-radius': corner,
	r'opacity': opacity,
}

settings = {
	'MEDIA': 'MEDIA_ROOT',
}
r'\b(opacity):(\s*)([^;]);'
