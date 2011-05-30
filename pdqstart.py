import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	f = open('index.html','r')
    	page = f.read()
    	f.close()
    	#"<img src='https://github.com/drahmel/PDQueue/blob/master/pdq-logo.png?raw=true' /><br/>PDQueue Started"
        self.write(page)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(7000)
    tornado.ioloop.IOLoop.instance().start()
