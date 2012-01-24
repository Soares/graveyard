#!/usr/local/bin/python3
import logger
import core

def initialize():
	core.vee = core.Vee()


def run():
	core.vee.run()


def main():
	initialize()
	run()


def profile(statement):
	import profile, pstats
	datafile = 'meta/profile.data'
	statfile = 'meta/profile.output'
	profile.run('main()', datafile)
	with open(statfile, 'w') as stream:
		p = pstats.Stats(datafile, stream=stream)
		p.strip_dirs().sort_stats('cumulative')
		p.print_stats()


def trace(statement):
	import trace
	tracer = trace.Trace(countfuncs=1, countcallers=1)
	tracer.run('main()')
	r = tracer.results()
	with open('meta/tracer.output', 'w') as stream:
		r.write_results(show_missing=True, coverdir='meta/covers/', stream=stream)


if __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option('-p', '--profile', dest='profile', action='store_true', help='Record profiling data', default=False)
	parser.add_option('-t', '--trace', dest='trace', action='store_true', help='Trace the execution of the program', default=False)
	options, args = parser.parse_args()

	statement = 'main()'
	if options.profile:
		statement = 'profile("{}")'.format(statement)
	if options.trace:
		statement = "trace('{}')".format(statement)
	exec(statement)
