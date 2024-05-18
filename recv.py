import http.server
import socketserver
import base64
import gzip
from io import BytesIO
import re

PORT = 3000

class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        encoded_string = self.path[1:]  # Skip the leading '/'
        try:
            decoded_data = base64.urlsafe_b64decode(encoded_string)

            if decoded_data[:2] == b'\x1f\x8b':  # Check for gzip magic number
                with gzip.GzipFile(fileobj=BytesIO(decoded_data)) as gzip_file:
                    decoded_string = gzip_file.read().decode('utf-8')  # Decompress and decode
            else:
                decoded_string = decoded_data.decode('utf-8')  # Directly decode

            # Function to perform the substitution
            def replace_match(match):
                print("match is:",match)
                translation_table = str.maketrans("LMNOPQRSTU", "0123456789")
                return match.group(0).translate(translation_table)

            # Regex to find all patterns that start with 'P' and are 14 capital letters long
            pattern = re.compile(r'P[A-Z]{15}')
            modified_string = pattern.sub(replace_match, decoded_string)

            print(modified_string, end='')
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
