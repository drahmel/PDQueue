#!/usr/bin/env python

import os.path
import re
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import memcache

from tornado.options import define, options

define("port", default=7000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler),
			(r"/job/([0-9a-zA-Z_]+)", JobHandler),

		]
		settings = dict(
			blog_title=u"PDQueue Admin",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
		)
		tornado.web.Application.__init__(self, handlers, **settings)
		self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)


class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db
	def mc(self):
		return self.application.mc

class HomeHandler(BaseHandler):
	def get(self):
		f = open('index.html','r')
		page = f.read()
		f.close()
		#"<img src='https://github.com/drahmel/PDQueue/blob/master/pdq-logo.png?raw=true' /><br/>PDQueue Started"
		self.write(page)
class JobHandler(BaseHandler):
	def get(self,jobname):
		mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		mkey = 'job_access_'+str(jobname)
		mc.add(mkey, "1")
		total = mc.incr(mkey)

		mkey = 'job_'+str(jobname)
		job_info = mc.get(mkey)
		self.write('Info on job: <b>'+str(jobname)+'</b> has '+str(total)+' accesses')
		if(len(job_info)>0):
			self.write('<hr/>'+str(job_info)+'<hr/>')
		self.write('<html><body><form action="/job/'+jobname+'" method="post">'
				   '<input type="text" name="message">'
				   '<input type="submit" value="Submit">'
				   '</form></body></html>')
		

	def post(self,jobname):
		mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		mkey = 'job_'+str(jobname)
		mc.set(mkey, self.get_argument("message"))
		self.set_header("Content-Type", "text/plain")
		self.write("You posted " + self.get_argument("message")+" to job "+jobname)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()

