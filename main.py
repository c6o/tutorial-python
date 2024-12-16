import http.server
import socketserver
import http.client
import logging

logging.basicConfig(level=logging.INFO)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        user_id = self.headers.get('x-c6o-userid')
        logging.info(f"Request from {self.client_address[0]}, userID={user_id}")

        try:
            conn = http.client.HTTPConnection("service-c", 8080)
            headers = {"x-c6o-userid": user_id}
            conn.request("GET", "/", headers=headers)
            response = conn.getresponse()
            if response.status != 200:
                raise Exception(f"HTTP request failed with status {response.status}")
            body = response.read()[:20]
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
            return

        logging.info(f"Sent response to {self.client_address[0]}, userID={user_id}: {body}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    PORT = 8080
    with socketserver.TCPServer(('127.0.0.1', PORT), MyHandler) as httpd:
        logging.info(f"Serving on port {PORT}")
        httpd.serve_forever()