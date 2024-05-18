import http.server
import socketserver
import base64
import gzip
from io import BytesIO

PORT = 3000

class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        encoded_string = self.path[1:] 
        try:
            decoded_data = base64.urlsafe_b64decode(encoded_string)

            if decoded_data[:2] == b'\x1f\x8b':
                with gzip.GzipFile(fileobj=BytesIO(decoded_data)) as gzip_file:
                    decoded_string = gzip_file.read().decode('utf-8')
                print(decoded_string, end='')
            else:
                decoded_string = decoded_data.decode('utf-8')
                print(decoded_string, end='')
        except Exception as e:
            print("Error decoding and/or unzipping Base64:", e)
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        pass

class MyTCPServer(socketserver.TCPServer):

    allow_reuse_address = True

def run(server_class=MyTCPServer, handler_class=MyHTTPHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Listening on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Server closed.")

if __name__ == "__main__":
    run()
