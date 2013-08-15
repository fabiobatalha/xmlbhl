import os

from tornado import (httpserver,
                     httpclient,
                     ioloop,
                     options,
                     web,
                     gen)

from tornado.options import (define,
                             options)

import tornado

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler)]

        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"))

        # Local is the default the default way that ratchet works.
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        data = {}
        data['status'] = 'alert-info'
        data['message'] = "choose a file to upload!"

        self.render("index.html", data=data)

    def post(self):
        data = {}
        if 'isofile' in self.request.files:
            isofile = self.request.files['isofile'][0]
            original_fname = isofile['filename']
            extension = original_fname.split('.')[-1]
            if isofile['content_type'] != u'application/octet-stream' and not extension in ['iso', 'part']:
                data['status'] = 'alert-danger'
                data['message'] = "file %s with content-type or extension not allowed. Please, upload files with valid extension (.iso, .part)." % original_fname
            else:
                try:
                    output_file = open("uploads/" + original_fname, 'wb')
                    output_file.write(isofile['body'])
                    data['status'] = 'alert-success'
                    data['message'] = "file %s is uploaded" % original_fname
                except IOError:
                    data['status'] = 'alert-danger'
                    data['message'] = "IOError trying to record: %s" % original_fname
        else:
            data['status'] = 'alert-danger'
            data['message'] = "You must select a valid file"

        self.render("index.html", data=data)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
