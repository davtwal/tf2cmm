'''
Root Python TF2CMM Server Module
Date: 5/24/2020
Usage: 
  Linux:    python3 server.py
  Windows:  py server.py

OR make run with the included makefile
'''

import os
import cherrypy
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tf2cmm.settings')
os.environ.setdefault('TF2CMM_HOST_IP', '127.0.0.1')
os.environ.setdefault('TF2CMM_HOST_PORT', '8001')

django.setup()

# These imports must be AFTER django.setup
from tf2cmm.wsgi import application
from django.conf import settings


# Cherrypy engine configuration.
engine_conf = {
  'server.socket_host': os.environ['TF2CMM_HOST_IP'],
  'server.socket_port': int(os.environ['TF2CMM_HOST_PORT']),
  'engine.autoreload_on': False,
  'log.screen': True
}

# Cherrypy 
tree_conf = {
  'tools.staticdir.on': True,
  'tools.staticdir.dir': settings.STATIC_ROOT,
  'tools.expires.on': True,
  'tools.expires.secs': 86400
}

def main():
  '''Main function used to start the server.'''
  cherrypy.log("Updating engine configuration...")
  cherrypy.config.update(engine_conf)

  cherrypy.log("Loading initial mount...")
  cherrypy.tree.mount(None, settings.STATIC_URL, {'/': tree_conf})

  cherrypy.log("Grafting Django WSGI Application...")
  cherrypy.tree.graft(application)

  # Cherrypy doesn't automatically subscribe this signal handler to the engine bus
  # when using engine.start(), only when using server.quickstart() - which we aren't using -
  # so in order to capture signals (e.g. SIGINT from Ctrl+C), subscribe the handler.
  if hasattr(cherrypy.engine, 'signal_handler'):
    cherrypy.engine.signal_handler.subscribe()

  # HOWEVER, the event is DIFFERENT for Windows computers, which is a DIFFERENT signal.
  # Of course. For this, we need to subscribe a win32 console ctrl handler plugin.
  if os.name == 'nt': # e.g. Windows_NT. Nice try.
    cherrypy.process.win32.ConsoleCtrlHandler(cherrypy.engine).subscribe()

  cherrypy.log("Loading engine...")
  cherrypy.engine.start()
  cherrypy.engine.block()

if __name__ == '__main__':
  main()
