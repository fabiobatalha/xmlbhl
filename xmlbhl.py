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
import tools
import models
import datetime

from sqlalchemy.exc import IntegrityError

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [(r"/", IndexHandler),
                    (r"/d/(\d+)", DeleteHandler), ]

        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"))

        Session = models.Session
        Session.configure(bind=models.engine)
        self.session = Session()

        # Local is the default the default way that ratchet works.
        tornado.web.Application.__init__(self, handlers, **settings)


class DeleteHandler(tornado.web.RequestHandler):

    @property
    def session(self):
        self._session = self.application.session
        return self._session

    def get(self, upload_id):
        data = {}

        try:
            data['status'] = 'alert-success'
            data['message'] = 'the file was removed'
            self.session.query(models.Upload).filter(models.Upload.id == upload_id).delete(synchronize_session=False)
            self.session.commit()
        except:
            self.session.rollback()
            data['status'] = 'alert-danger'
            data['message'] = "the file could not be removed, or was already removed"

        data['uploaded_files'] = self.session.query(models.Upload).all()

        self.render("index.html", data=data)


class IndexHandler(tornado.web.RequestHandler):

    @property
    def session(self):
        self._session = self.application.session
        return self._session

    def get(self):
        data = {}
        data['status'] = 'alert-info'
        data['message'] = "choose a file to upload!"
        data['uploaded_files'] = self.session.query(models.Upload).all()

        self.render("index.html", data=data)

    def post(self):
        data = {}
        if 'isofile' in self.request.files:
            isofile = self.request.files['isofile'][0]
            original_fname = isofile['filename']
            if tools.is_valid_file(isofile):
                try:
                    save_as = "uploads/" + original_fname
                    output_file = open(save_as, 'wb')
                    output_file.write(isofile['body'])
                    data['status'] = 'alert-success'
                    data['message'] = "file %s was uploaded" % original_fname

                    source = tools.get_json(save_as)

                    upload = models.Upload(original_fname,
                                           datetime.datetime.now().isoformat(),
                                           source)
                    self.session.add(upload)
                    self.session.commit()
                except IOError:
                    data['status'] = 'alert-danger'
                    data['message'] = "IOError trying to record: %s" % original_fname
                except IntegrityError:
                    self.session.rollback()
                    data['status'] = 'alert-danger'
                    data['message'] = "Please check if the file already exists, you must remove it before upload again the same file: %s" % original_fname

            else:
                data['status'] = 'alert-danger'
                data['message'] = "file %s with content-type or extension not allowed. Please, upload files with valid extension (.iso, .part)." % original_fname
        else:
            data['status'] = 'alert-danger'
            data['message'] = "You must select a file"

        data['uploaded_files'] = self.session.query(models.Upload).all()

        self.render("index.html", data=data)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
