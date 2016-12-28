"""Mite input utilities."""
import sys

def confirm(prompt=None, default=False):
	"""
	Prompts for yes (True) or no (False) response from the user.
	Set 'default' to True to default to yes.
	"""
	prompt = prompt or 'Are you sure?'
	confirm = '*[yn] ' if default else '[yn]* '

	print(prompt, confirm, end='')
	while True:
		response = input()
		if not response:
			return default
		if response in 'yY':
			return True
		if response in 'nN':
			return False
		sys.stderr.write('\a')
