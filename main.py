import sys
sys.path.append('./')
from mkid import mkid

from json import dumps as jsonify
from json import loads as unjsonify

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
  def get(self, id):
    if not id:
      template = jinja_env.get_template('index.html')
      self.response.write(template.render())
    else:
      key = ndb.Key('Url', id)
      entity = key.get()
      if entity:
        url = entity.url
        if url[:4].lower() != 'http':
          url = 'http://' + url
          return webapp2.redirect(url, abort=True)
      else:
        self.response.write('url does not exist')
    self.response.write('this shouldnt happen')



  def post(self, id=None):
    #self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    longurl = self.request.get('longurl')
    tinyurl = mkid(cannot_be = ['api', 'contact', 'about', 'login'])
    if ndb.Key('Url', tinyurl).get() is not None:
      return self.response.write('url already exists. my bad.')

    url = Url()
    url.url = longurl
    url.tinyurl = tinyurl
    url.ip = self.request.remote_addr
    url.key = ndb.Key(Url, tinyurl)
    url.put()
    del url
    return self.response.write(jsonify({'id' : tinyurl}))

# class GetUrl(webapp2.RequestHandler):

#   def get(self):
#     print 'we get home'

#     return self.response.write('%s' % tinyurl)

#   def post(self):
#     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
#     longurl = self.request.get('longurl')
#     tinyurl = mkid(cannot_be = ['api', 'contact', 'about', 'login'])
#     if ndb.Key('Url', tinyurl).get() is not None:
#       return
#       # tinyurl id exists

#     url = Url()
#     url.url = longurl
#     url.tinyurl = tinyurl
#     url.ip = self.request.remote_addr
#     url.key = ndb.Key(Url, tinyurl)
#     url.put()
#     del url
#     return self.response.write(jsonify({'id' : tinyurl}))



routes = [
  ('/(.+)?', Home)

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