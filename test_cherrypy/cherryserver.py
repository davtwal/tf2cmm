'''Cherrypy test server'''
import os
import os.path
import random
import string

import sqlite3
import time

import cherrypy

DB_STRING = "my.db"

class StringGenerator:
  def __init__(self, generator=None):
    self.generator = generator

  @cherrypy.expose
  def index(self):
    return open('index.html')

@cherrypy.expose
class StringGeneratorWebService:
  @cherrypy.tools.accept(media='text/plain')
  def GET(self):
    with sqlite3.connect(DB_STRING) as con:
      cherrypy.session['ts'] = time.time()
      resp = con.execute("SELECT value FROM user_string WHERE session_id=?",
                         [cherrypy.session.id])
      return resp.fetchone()

  def POST(self, length=8):
    some_str = ''.join(random.sample(string.hexdigits, int(length)))
    with sqlite3.connect(DB_STRING) as con:
      cherrypy.session['ts'] = time.time()
      con.execute("INSERT INTO user_string VALUES (?, ?)",
                  [cherrypy.session.id, some_str])
    return some_str

  def PUT(self, another_string):
    with sqlite3.connect(DB_STRING) as con:
      cherrypy.session['ts'] = time.time()
      con.execute("UPDATE user_string SET value=? WHERE session_id=?",
                  [another_string, cherrypy.session.id])

  def DELETE(self):
    cherrypy.session.pop('ts', None)
    with sqlite3.connect(DB_STRING) as con:
      con.execute("DELETE FROM user_string WHERE session_id=?",
                  [cherrypy.session.id])

def setup_database():
  with sqlite3.connect(DB_STRING) as con:
    con.execute("CREATE TABLE user_string (session_id, value)")

def cleanup_database():
  with sqlite3.connect(DB_STRING) as con:
    con.execute("DROP TABLE user_string")

def main():
  cherrypy.engine.subscribe('start', setup_database)
  cherrypy.engine.subscribe('stop', cleanup_database)

  webapp = StringGenerator(StringGeneratorWebService())
  cherrypy.quickstart(webapp, '/', 'app.conf')

if __name__ == '__main__':
  main()
