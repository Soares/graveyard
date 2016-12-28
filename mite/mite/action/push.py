"""Mite push built site to git branch."""
import argparse
import os
import logging
import subprocess
import sys

import mite
import mite.action.base


KEYWORD = 'push'


class Action(mite.action.base.Action):
	"""Push built site to git branch."""

	def flagparser(self, prog, keyword):
		parser = argparse.ArgumentParser(prog='{} {}'.format(prog, keyword))
		parser.add_argument(
				'branch',
				nargs='?',
				default='gh-pages',
				metavar='BRANCH',
				help="""
				The git branch to push to.
				Only the compiled site (usually found in .build) will be pushed.
				Default: gh-pages.
				""")
		mite.action.base.add_site_flag(parser)
		return parser

	def execute(self):
		super().execute()
		push(self.config.builddir, self.branch)


def push(builddir, branch):
	"""
	Push only the build directory to a git branch which should contain only the
	build directory (i.e. gh-pages).
	"""
	current = current_branch_or_die()
	branchref = os.path.join('refs', 'heads', branch)
	if os.path.exists(os.path.join('.git', branchref)):
		with open(os.path.join('.git', branchref)) as reffile:
			parent = reffile.read().rstrip('\n')
	else:
		logging.info('Creating branch {}'.format(branch))
		parent = None
	tree = '%s^{tree}:%s' % (current, builddir)
	message = 'Pushing to {0} from {1}'.format(branch, current)
	command = ['git', 'commit-tree', tree, '-m', message]
	if parent:
		command += ['-p', parent]
	try:
		commit = subprocess.check_output(command)
	except subprocess.CalledProcessError:
		print("Couldn't push {}. Is it in .gitignore?".format(
			builddir), file=sys.stderr)
		sys.exit(0)
	else:
		commit = commit.decode('utf-8').rstrip('\n')
	subprocess.check_call(['git', 'update-ref', branchref, commit])
	logging.info('Pushed {build} to {branch} from {current}'.format(
		build=builddir,
		branch=branch,
		current=current))


def current_branch_or_die():
	"""Get the current git branch or die trying."""
	try:
		branch = subprocess.check_output([
			'git','rev-parse',
			'--abbrev-ref', 'HEAD'])
	except subprocess.CalledProcessError:
		raise mite.NotCurrentlyPossible(
				"You don't appear to be on a git branch.")
	return branch.decode('utf-8').rstrip('\n')
