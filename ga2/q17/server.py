from http.server import HTTPServer, BaseHTTPRequestHandler

EMAIL = "your-student-id"  # replace with your student id

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"<html><body><h1>{EMAIL}</h1></body></html>".encode("utf-8"))

def run(server_class=HTTPServer, handler_class=MyHandler, port=3000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
