#!/usr/bin/env python
 
import os, sys, time
from subprocess import Popen, PIPE
from daemon_class import Daemon
 
class MyDaemon(Daemon):
        def run(self):
                # Creamos el log del daemon
                archivo_log = open("/var/log/monitorappsd_log", "w")
                archivo_log.close()
                while True:
                        archivo_log = open("/var/log/monitorappsd_log", "a")
                        
                        archivo_log.write('\n--------------------------------\n')

                        proceso_date = Popen("date", stdout=PIPE)
                        
                        out, err = proceso_date.communicate()
                        
                        archivo_log.write(out.decode('utf-8')+'\n')

                        aplicaciones = ['mate-terminal', 'pluma', 'mate-calc']

                        for app in aplicaciones:
                        
                            # Vamos a hacer esto: ps -aux | grep "mate-calc" | grep -v "grep"
                            
                            # Ejecutamos el comando 'ps' y redirigimos su salida a un pipe.
                            proceso_ps = Popen(["ps", "-aux"], stdout=PIPE)
                            
                            # Ejecutamos el comando 'grep' tomando como entrada el pipe anterior y redirigiendo la salida a otro pipe.
                            proceso_grep = Popen(["grep", app], stdin=proceso_ps.stdout, stdout=PIPE)
                            
                            # Ejecutamos nuevamente el comando 'grep' para excluir los resultados que incluyan al 'grep' anterior.
                            proceso_grep_reverso = Popen(["grep", "-v", "grep"], stdin=proceso_grep.stdout, stdout=PIPE)
                            
                            out, err = proceso_grep_reverso.communicate()
                            
                            if out:
                                archivo_log.write(f'{app}: SÍ se está ejecutando.\n')
                                archivo_log.write(out.decode('utf-8')+'\n')
                            else:
                                archivo_log.write(f'{app}: NO se está ejecutando.\n')
                            
                        archivo_log.close()
                        
                        time.sleep(5)
 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/monitorappsd.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                        # Eliminamos el log para la siguiente ejecución.
                        os.remove("/var/log/monitorappsd_log")
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)

