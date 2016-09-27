# composite indexes won't work if a property is has indexed=False

from google.appengine.ext import ndb
class Url(ndb.Model):
  url = ndb.StringProperty(indexed=False)
  tinyurl = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)
  ip = ndb.StringProperty()
