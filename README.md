# raw-http-server

A minimal HTTP server built from scratch in Python using only the built-in `socket` module — no Flask, no Django, no frameworks. This project exists to understand what web frameworks are actually doing under the hood: opening sockets, parsing raw HTTP text, and constructing responses by hand.

## Why this exists

Frameworks hide the actual mechanics of HTTP behind decorators and routing magic. This project strips all of that away to answer:

- What does a raw HTTP request actually look like as bytes on the wire?
- How does a server know where one request ends and the response begins?
- Where do "resources" (HTML, images, etc.) actually come from when a server responds?
- Why do we need things like `Content-Type` and `Content-Length` headers at all?

## How it works

1. Open a TCP socket and bind it to a local address/port.
2. Listen for incoming connections.
3. On each connection, read the raw bytes off the wire and decode them into the literal HTTP request text (e.g. `GET / HTTP/1.1`).
4. Parse out the requested path.
5. Look up a matching file on disk, read it in binary mode.
6. Hand-build an HTTP response: status line, headers, blank line, body.
7. Send the raw bytes back and close the connection.

No abstraction layer — every line above is explicit in the code.

## Running it

```bash
python3 server.py
```

Then open:

```
http://localhost:8080
```

The terminal running the server will print each raw incoming HTTP request as plain text — this is worth reading closely, it's the whole point of the exercise.

## Project structure

```
raw-http-server/
├── server.py        # the server itself
├── public/          # files the server can serve (HTML, images, etc.)
│   └── index.html
└── README.md
```

## What this server does NOT do (on purpose)

This is a learning tool, not a production server. It intentionally skips things real servers need:

- Handling multiple clients concurrently (one connection is processed at a time)
- Protection against path traversal attacks (e.g. requesting `../../etc/passwd`)
- HTTPS / TLS
- Timeouts, keep-alive connections, chunked transfer encoding
- Robust error handling for malformed requests

If you want a real server for production use, use nginx, Apache, or a proper framework. This project is about understanding what those tools are doing for you.

## What I learned

- HTTP is plain text over TCP — nothing magic about it.
- A server's "response" can be entirely hand-built as a string/bytes; there's no requirement to read from disk unless you choose to.
- `Content-Type` and `Content-Length` exist because the client has no other way to know how to interpret or where to stop reading the bytes it receives.
- Binary files (images, etc.) must be read and sent in binary mode — text mode will corrupt them.

## License

MIT — do whatever you want with it.












