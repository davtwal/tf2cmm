'''
  Party Web Service
'''

import cherrypy

from database import Database

@cherrypy.expose
class PartyWebService:
  '''Web service for party'''
  def __init__(self, database):
    self.db = database

  def GET(self, party_id, password=None):
    if party_id is None:
      pass # redirect to 'bad party' ?
    elif cherrypy.session['party_id'] is not None:
      pass # redirect to 'you are already in a party'?
    else:
      # check to see if the party exists in the database
      resp = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='?'", [party_id])
      if resp.fetchone() == 0:
        pass # redirect to 404 party not found
      party_pw = self.db.execute("SELECT password FROM parties WHERE party_id=?", [party_id]).fetchone()
      elif party_pw is not None and password != party_pw:
        pass # redirect to 404 party not found

      cherrypy.session['party_id'] = party_id
      self.db.execute("CREATE TABLE IF NOT EXISTS parties.? (session_id, pings)")
  
db = Database(cherrypy.engine, "my.db")
pws = PartyWebService(db)

