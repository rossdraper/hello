import http.server
import socketserver
import base64
import gzip
from io import BytesIO

PORT = 3000

class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Extract the Base64 encoded part from the URL path
        encoded_string = self.path[1:]  # skip the leading '/'
        try:
            # Attempt to decode the Base64 encoded string
            decoded_data = base64.urlsafe_b64decode(encoded_string)

            # Check if the data is gzipped by looking at the first two bytes
            if decoded_data[:2] == b'\x1f\x8b':
                with gzip.GzipFile(fileobj=BytesIO(decoded_data)) as gzip_file:
                    decoded_string = gzip_file.read().decode('utf-8')
                print("Decoded and Unzipped URL Argument:", decoded_string)
            else:
                decoded_string = decoded_data.decode('utf-8')
                print("Decoded URL Argument:", decoded_string)
        except Exception as e:
            print("Error decoding and/or unzipping Base64:", e)

        # Send a 404 response
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
#        self.wfile.write(b"404 Not Found")

class MyTCPServer(socketserver.TCPServer):
    # This allows the server to bind to the address and port even if it was recently used
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
