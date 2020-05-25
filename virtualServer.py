from sys import argv
import BaseHTTPServer
import os
from SimpleHTTPServer import SimpleHTTPRequestHandler , test
#
try:
    print("Getting port: {}".format(int(argv[1])))
except IndexError:
    print("Usage: virtualServer [port] [file]")
    print("Not given parameter   ^^^^")
    exit()
except ValueError:
    print("Usage: virtualServer [port] [file]")
    print("required integer      ^^^^")
    exit()
try:
    print("Serving file {}".format(argv[2]))
except IndexError:
    print("Usage: virtualServer [port] [file]")
    print("Not given parameter          ^^^^")
    exit()
class ComplexHTTPRequestHandler(SimpleHTTPRequestHandler):
    def send_head(self):
            path = self.translate_path(self.path)
            f = None
            if os.path.isdir(path):
                if not self.path.endswith('/'):
                    self.send_response(301)
                    self.send_header("Location", self.path + "/")
                    self.end_headers()
                    return None
                for index in str(argv[2]),"index.html":
                    index = os.path.join(path, index)
                    if os.path.exists(index):
                        path = index
                        break
                else:
                    return self.list_directory(path)
            ctype = self.guess_type(path)
            try:
                f = open(path, 'rb')
            except IOError:
                self.send_error(404, "File not found")
                return None
            try:
                self.send_response(200)
                self.send_header("Content-type", ctype)
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs[6]))
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.end_headers()
                return f
            except:
                f.close()
                raise
test(HandlerClass = ComplexHTTPRequestHandler,ServerClass = BaseHTTPServer.HTTPServer,filename=argv[2])