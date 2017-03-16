import BaseHTTPServer

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
        Handle the request and return page,inherit from BaseHTTPRequestHandler.
    '''

    # build the page model
    Page = '''\
        <html>
        <body>
            <table>
                <tr>  <td>Header</td>         <td>Value</td>          </tr>
                <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
                <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
                <tr>  <td>Client port</td>    <td>{client_port}</td> </tr>
                <tr>  <td>Command</td>        <td>{command}</td>      </tr>
                <tr>  <td>Path</td>           <td>{path}</td>         </tr>
            </table>
        </body>
        </html>
        '''

    # The get request
    def do_GET(self):
        page = self.create_page()
        self.send_content(page)

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
    def send_content(self,page):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length",str(len(self.Page)))
        self.end_headers()
        self.wfile.write(self.Page)        

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
