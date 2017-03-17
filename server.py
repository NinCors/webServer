import BaseHTTPServer,sys,os


# possible cases
cases = [case_no_file(),
        case_exostomg_file(),
        case_fail()]

# error handler
class ServerException(Exception):
    pass

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
        Handle the request and return page,inherit from BaseHTTPRequestHandler.
    '''

    # build the page 
    Error_Page = '''\
        <html>
            <body>
                <h1>Error accessing {path}</h1>
                <p>{msg}</p>
            </body>
        </html>
        '''

    # The get request
    def do_GET(self):
        try:
            full_path = os.getcwd() + self.path
            if not os.path.exists(full_path):
                raise ServerException("'{0}' not found".format(self.path))

            elif os.path.isfile(full_path):
                self.handle_file(full_path)

            else:
                raise ServerException("Unkown object '{0}'".format(self.path))

        except Exception as msg:
            self.handle_error(msg)
    
    def handle_file(self,full_path):
        try:
            with open(full_path,'rb') as file:
                content = file.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path,msg)
            self.handle_error(msg)

    def handle_error(self,msg): 
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content,404)

    def create_page(self):
        values = {
            'date_time' : self.date_time_string(),
            'client_host' : self.client_address[0],
            'client_port' : self.client_address[1],
            'command' : self.command,
            'path' : self.path
        }
        page = self.Page.format(**values)
        return page

    # Send the content based on the request
    def send_content(self,page,status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length",str(len(page)))
        self.end_headers()
        self.wfile.write(page)        


# cases: file not exited
class case_no_file(object):
    def test(self,handler):
        return not os.path.exists(handler.full_path)

    def act(self.handler):
        raise ServerException("'{0}' not found".format(handler.path))


# cases: the path is file
class case_existing_file(object):
    def test(self,handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        handler.handle_file(handler.full_path)

# cases: else
class case_fail(object):
    def test(self, handler):
        return True
    def act(self,handler):
        raise ServerException()





if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
