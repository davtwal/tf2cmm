'''
  Root of Server
  Author: David Walker
'''

import cherrypy

from database import Database

import time
import random
import string
@cherrypy.expose
class StringGenWebService:
  '''Web service for string generation'''
  def __init__(self, database):
    self.db = database

  @cherrypy.tools.accept(media='text/plain')
  def GET(self):
    '''Generator HTTP GET Request Handler'''
    cherrypy.session['ts'] = time.time()
    resp = self.db.execute("SELECT value FROM user_string WHERE session_id=?",
                           [cherrypy.session.id])
    return resp.fetchone()

  def POST(self, length=8):
    '''Generator HTTP POST Request Handler'''
    some_str = ''.join(random.sample(string.hexdigits, int(length)))
    cherrypy.session['ts'] = time.time()
    self.db.execute("INSERT INTO user_string VALUES (?, ?)",
                    [cherrypy.session.id, some_str])
    return some_str

  def PUT(self, another_str):
    cherrypy.session['ts'] = time.time()
    self.db.execute("UPDATE user_string SET value=? WHERE session_id=?",
                    [another_str, cherrypy.session.id])
  
  def DELETE(self):
    cherrypy.session.pop('ts', None)
    self.db.execute("DELETE FROM user_string WHERE session_id=?", [cherrypy.session.id])

class Root:
  @cherrypy.expose
  def index(self):
    return open('index.html')

def main():
  '''Main function'''
  main_db = Database(cherrypy.engine, 'database.db')
  main_db.subscribe()

  app = Root()
  app.generator = StringGenWebService(main_db)

  cherrypy.quickstart(app, '/', 'app.conf')

if __name__ == '__main__':
  main()
