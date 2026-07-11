# Build a raw HTTP server in Python — no Django, no frameworks
# Just Python's built-in socket library
import socket
import os

HOST = 'localhost'
PORT = 8080
PUBLIC_DIR = 'public'

# Map file extensions to Content-Type headers.
# The browser relies on this to know how to interpret the bytes it gets back.
CONTENT_TYPES = {
    '.html': 'text/html',
    '.htm':  'text/html',
    '.css':  'text/css',
    '.js':   'text/javascript',
    '.jpg':  'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png':  'image/png',
    '.gif':  'image/gif',
    '.txt':  'text/plain',
}

def get_content_type(filename):
    _, ext = os.path.splitext(filename)
    return CONTENT_TYPES.get(ext, 'application/octet-stream')  # fallback = "just bytes"

def build_response(status, content_type, body):
    """Build a full raw HTTP response as bytes: status line + headers + blank line + body."""
    header = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
    )
    return header.encode() + body

def handle_request(request_text):
    """Parse the raw request text, load the matching file, return response bytes."""
    try:
        first_line = request_text.split('\r\n')[0]      # e.g. "GET /about.html HTTP/1.1"
        method, path, version = first_line.split(' ')
    except (ValueError, IndexError):
        body = b"<h1>400 Bad Request</h1>"
        return build_response("400 Bad Request", "text/html", body)

    # Default to index.html for the root path
    if path == '/':
        path = 'public/index.html'

    # NOTE: no path-traversal protection here on purpose — see README for what's
    # intentionally left out of this learning project.
    filename = os.path.join(PUBLIC_DIR, path.lstrip('/'))

    try:
        with open(filename, 'rb') as f:   # 'rb' = binary mode, required for images etc.
            body = f.read()
        content_type = get_content_type(filename)
        return build_response("200 OK", content_type, body)
    except FileNotFoundError:
        body = b"<h1>404 Not Found</h1>"
        return build_response("404 Not Found", "text/html", body)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow quick restarts without "Address already in use" errors
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Serving {PUBLIC_DIR}/ on http://{HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode(errors='replace')
        print(request)  # See raw HTTP

        if request:  # ignore empty requests (e.g. some browsers probe with a blank connection)
            response = handle_request(request)
            conn.send(response)

        conn.close()

if __name__ == '__main__':
    main()