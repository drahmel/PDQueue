#!/usr/bin/env python

import os.path
import re
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from tornado.options import define, options

define("port", default=7000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler)
        ]
        settings = dict(
            blog_title=u"PDQueue Admin",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        pass

class HomeHandler(BaseHandler):
    def get(self):
    	f = open('index.html','r')
    	page = f.read()
    	f.close()
    	#"<img src='https://github.com/drahmel/PDQueue/blob/master/pdq-logo.png?raw=true' /><br/>PDQueue Started"
        self.write(page)

application = tornado.web.Application([
    (r"/", HomeHandler),
])

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

