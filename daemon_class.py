
import sys, os, time, atexit, signal

class Daemon:

	def __init__(self, pidfile): self.pidfile = pidfile
	
	def daemonize(self):
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit del parent
				sys.exit(0) 
		except OSError as err: 
			sys.stderr.write('fork #1 failed: {0}\n'.format(err))
			sys.exit(1)
	
		# desacople 
		os.chdir('/') 
		os.setsid() 
		os.umask(0) 
	
		# segundo fork
		try: 
			pid = os.fork() 
			if pid > 0:

				# exit del segundo parent
				sys.exit(0) 
		except OSError as err: 
			sys.stderr.write('fork #2 failed: {0}\n'.format(err))
			sys.exit(1) 
	
		# Redireccionamos estandar imput y output 
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(os.devnull, 'r')
		so = open(os.devnull, 'a+')
		se = open(os.devnull, 'a+')

		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# Al terminar, borramos pidfile
		atexit.register(self.delpid)

		# Escribimos el pid en pidfile
		pid = str(os.getpid())
		with open(self.pidfile,'w+') as f:
			f.write(pid + '\n')
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):

		# Chequeamos pidfile para ver si el daemon ya estaba corriendo
		try:
			with open(self.pidfile,'r') as pf:

				pid = int(pf.read().strip())
		except IOError:
			pid = None
	
		if pid:
			message = "pidfile {0} already exist. " + \
					"Daemon already running?\n"
			sys.stderr.write(message.format(self.pidfile))
			sys.exit(1)
		
		# Start daemon
		self.daemonize()
		self.run()

	def stop(self):
		# Tomamos el pid del pidfile
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None
	
		if not pid:
			message = "pidfile {0} does not exist. " + \
					"Daemon not running?\n"
			sys.stderr.write(message.format(self.pidfile))
			return 

		# Kill del proceso	
		try:
			while 1:
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			e = str(err.args)
			if e.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print (str(err.args))
				sys.exit(1)

	def restart(self):
		self.stop()
		self.start()

	def run(self):
		# Sobreescribir este metodo
		""""""

