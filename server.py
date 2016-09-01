import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
import urls
import os.path
from tornado import autoreload
# import app

class Application(tornado.web.Application):
    def __init__(self):

        handlers = urls.handlers

        settings = dict(
            title=u"Ed's Website",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url="/login",
            cookie_secret='yM8d59GwSSeF4b2Zj+O37WMO1EHzJ0yKiiFgZR3jS0s=',
        )

        tornado.web.Application.__init__(self, handlers, **settings)
        #self._app = app.SHARED_APPLICATION
        #self.db = self._app.mysqldb
        #self.mysqldb = self.db


def main():
    from tornado.httpserver import HTTPServer
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    real_port = 3000
    http_server.listen(real_port)
    print('Listening at port %s' % real_port)

    ioloop = tornado.ioloop.IOLoop.instance()
    autoreload.start(ioloop)
    ioloop.start()

    # #app = make_app()
    # server = tornado.httpserver.HTTPServer(Application())
    # real_port = 3000
    # server.bind(real_port)
    # # server.start(0)  # forks one process per cpu
    # #tornado.ioloop.IOLoop.current().start()
    # print('Listening at port %s' % real_port)

    # ioloop = tornado.ioloop.IOLoop.instance()
    # autoreload.start(ioloop)
    # ioloop.start()

if __name__ == "__main__":
    main()