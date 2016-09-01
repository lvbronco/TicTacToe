import tornado.web
import urllib
import urlparse
from tornado.escape import json_decode
from validationmixin import ValidationMixin

class BaseHandler(tornado.web.RequestHandler, ValidationMixin):
    @property
    def db(self):
        return self.application.db

    @property
    def mysqldb(self):
        return self.application.mysqldb

    def forbidden(self):
        url = self.get_login_url()
        if "?" not in url:
            if urlparse.urlsplit(url).scheme:
                # if login url is absolute, make next absolute too
                next_url = self.request.full_url()
            else:
                next_url = self.request.uri
            url += "?" + urllib.urlencode(dict(next=next_url))
        self.redirect(url)

    def prepare(self):
        """
            If contentType is application/json, then set arguments to decoded dictionary.
        """
        if 'Content-Type' in self.request.headers:
            content_type = self.request.headers['Content-Type']
            if content_type == "application/json":
                print 'json data'
                data = self.request.body
                try:
                    json_data = json_decode(data)
                except ValueError:
                    raise tornado.httpserver._BadRequestException(
                        "Invalid JSON structure."
                    )
                if type(json_data) != dict:
                    raise tornado.httpserver._BadRequestException(
                        "We only accept key value objects!"
                    )
                for key, value in json_data.iteritems():
                    self.request.arguments[key] = [unicode(value),]

    def write_error(self, status_code, **kwargs):
        if 'chunk' in kwargs:
            self.write(kwargs['chunk'])

    def send_errors(self):
        return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : self.errors })


    def send_ok(self):
        return self.write({'Status' : 'OK'})
