'''
  Database Module
  Author: David Walker
'''
import sqlite3 as db
from cherrypy.process.plugins import SimplePlugin

class IDatabase(SimplePlugin):
  def __init__(self, bus, db_name):
    SimplePlugin.__init__(self, bus)
    self.db_name = db_name

  def __connect(self):
    '''
    Connects to the database, returning the connection object.
    Intended to be used as so: with self.connect() as con
    Private internal function
    '''
    pass

class Database(SimplePlugin):
  '''
  Database Base Class
  '''
  def __init__(self, bus, db_name):
    SimplePlugin.__init__(self, bus)
    self.db_name = db_name

  def __connect(self):
    '''
    Connects to the database, returning the connection object.
    Intended to be used as so: with self.connect() as con
    Private internal function
    '''
    return db.connect(self.db_name)

  def start(self):
    '''
    Creates the database
    '''
    self.bus.log('Database created')
    with self.__connect() as con:
      con.execute("CREATE TABLE user_string (session_id, value)")

  def stop(self):
    '''
    Shuts down the database
    '''
    self.bus.log('Database dropped')
    with self.__connect() as con:
      con.execute("DROP TABLE user_string")

  def execute(self, command, params):
    '''Executes a command to the database. Returns the response'''
    with self.__connect() as con:
      return con.execute(command, params)
