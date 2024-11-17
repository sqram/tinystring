import sys
sys.path.append('./')
from mkid import mkid

from json import dumps as jsonify
from json import loads as unjsonify
from os.path import dirname

import jinja2
import webapp2
from google.appengine.ext import ndb
#from webapp2_extras import sessions, sessions_memcache, sessions_ndb

from models.url import Url

jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(
  dirname(__file__)+'/templates/'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class Home(webapp2.RequestHandler):
  def get(self):

    template = jinja_env.get_template('index.html')
    self.response.write(template.render())

  def post(self, id=None):
    longurl = self.request.get('longurl')
    tinyurl = mkid(cannot_be = ['api'])
    if ndb.Key('Url', tinyurl).get() is not None:
      return self.response.write("url already exists. my bad. bug in code i'm not willing to fix for this tiny project.")

    url = Url()
    url.url = longurl
    url.tinyurl = tinyurl
    url.ip = self.request.remote_addr
    #url.key = ndb.Key(Url, tinyurl)
    url.put()
    del url
    return self.response.write(jsonify({'id' : tinyurl}))

class GetUrl(webapp2.RequestHandler):
  def get(self, tinyurl):
    entity = Url.query(Url.tinyurl == tinyurl).get() 
    if entity:
      url = entity.url
      if url[:4].lower() != 'http':
        url = 'http://' + url
      return webapp2.redirect(url, abort=True)
    else:
      return self.response.write('url does not exist')

  def post(self):
    return self.response.write('no posting')



routes = [
  ('/', Home),
  ('/(.+)?', GetUrl)
]

conf = {

}


app = webapp2.WSGIApplication(routes=routes,  debug=True)


def render(template, templatedata = {}, spfdata = {}, spf=''):
  template = jinja_env.get_template(template + '.html')
  if spf:
    templatedata['full'] = False
    spfdata['body'] = {'content': template.render(**templatedata) }
    return jsonify(spfdata)
  else:
    return template.render(**templatedata)