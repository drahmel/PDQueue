#!/usr/bin/env python

import os.path
import re
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import time, random

from Cache import *
from c import *

from tornado.options import define, options

define("port", default=7000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler),
			(r"/job/([0-9a-zA-Z_]+)", JobHandler),
			(r"/longpoll/([0-9a-zA-Z_]+)", LongPollHandler),

		]
		settings = dict(
			blog_title=u"PDQueue Admin",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
		)
		tornado.web.Application.__init__(self, handlers, **settings)
		#self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)


class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

class HomeHandler(BaseHandler):
	def get(self):
		f = open('index.html','r')
		page = f.read()
		f.close()
		#"<img src='https://github.com/drahmel/PDQueue/blob/master/pdq-logo.png?raw=true' /><br/>PDQueue Started"
		self.write(page)
		mkey = "cron_check"
		cronCheckCount = Cache.get(mkey)
		self.write("Current # of cronChecks: "+str(cronCheckCount))
		
class JobHandler(BaseHandler):
	def get(self,jobname):
		mkey = 'job_access_'+str(jobname)
		total = Cache.inc(mkey)

		mkey = 'job_'+str(jobname)
		job_info = Cache.get(mkey)
		self.write('Info on job: <b>'+str(jobname)+'</b> has '+str(total)+' accesses')
		if(len(job_info)>0):
			self.write('<hr/>'+str(job_info)+'<hr/>')
		self.write('<html><body><form action="/job/'+jobname+'" method="post">'
				   '<input type="text" name="message">'
				   '<input type="submit" value="Submit">'
				   '</form></body></html>')
		

	def post(self,jobname):
		mkey = 'job_'+str(jobname)
		Cache.set(mkey, self.get_argument("message"))
		self.set_header("Content-Type", "text/plain")
		self.write("You posted " + self.get_argument("message")+" to job "+jobname)
		
class LongPollHandler(BaseHandler):
	def get(self,polltype):
		if(polltype=='send'):
			items = ["Item 1", "Item 2", "Item 3"]
			random.shuffle(items)
			pollitem = items[0]
			self.render("longpoll.html", title="Long Polling example", items=items, pollitem=pollitem)
		else:
			time.sleep(10)
			items = ["cheese", "bacon", "sausage", "pineapple", "pepperoni", "extra sauce"]
			random.shuffle(items)
			pollitem = items[0]
			self.write('{"type":"'+str(pollitem)+'"}')

def cronCheck():
	mkey = "cron_check"
	total = Cache.inc(mkey)
	#print total

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tInstance = tornado.ioloop.IOLoop.instance()
	# Add cronCheck callback to check cron schedule every minute
	checkmilli = 60000
	scheduler = tornado.ioloop.PeriodicCallback(cronCheck, checkmilli, io_loop=tInstance)
	# Start scheduler
	scheduler.start()
	# Start Tornado
	tInstance.start()


if __name__ == "__main__":
	main()

