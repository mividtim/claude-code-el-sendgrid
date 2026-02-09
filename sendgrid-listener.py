"""SendGrid Inbound Parse webhook listener for claude-code-event-listeners.

Blocks until an email arrives via SendGrid's Inbound Parse, outputs JSON
to stdout, exits. Handles multipart form data from SendGrid.

Usage: python3 sendgrid-listener.py [port]
"""
import json, os, sys, email
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9998

WATERMARK_FILE = os.environ.get('SENDGRID_WATERMARK_FILE', '/tmp/sendgrid-webhook-watermark')


def parse_multipart(headers, body):
    """Parse multipart/form-data from SendGrid Inbound Parse."""
    content_type = headers.get('Content-Type', '')
    # Build a full email message for parsing
    msg = email.message_from_string(
        f"Content-Type: {content_type}\r\n\r\n" + body
    )
    if msg.is_multipart():
        fields = {}
        for part in msg.walk():
            name = part.get_param('name', header='content-disposition')
            if name:
                fields[name] = part.get_payload(decode=True).decode('utf-8', errors='replace')
        return fields
    # Fallback: URL-encoded
    return {k: v[0] for k, v in parse_qs(body).items()}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SendGrid Inbound Parse listener ready\n")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8', errors='replace')

        fields = parse_multipart(self.headers, body)

        # Respond to SendGrid immediately
        self.send_response(200)
        self.end_headers()
        self.wfile.flush()

        # Extract email fields
        from_addr = fields.get('from', '')
        to_addr = fields.get('to', '')
        subject = fields.get('subject', '')
        text = fields.get('text', '')
        html = fields.get('html', '')

        # Watermark check — skip if we've already seen this
        msg_id = fields.get('Message-ID', fields.get('message-id', ''))

        output = {
            'from': from_addr,
            'to': to_addr,
            'subject': subject,
            'text': text,
            'message_id': msg_id,
        }
        if html and not text:
            output['html'] = html

        # Update watermark
        try:
            with open(WATERMARK_FILE, 'w') as f:
                f.write(msg_id or subject)
        except Exception:
            pass

        print(json.dumps(output), flush=True)
        os._exit(0)

    def log_message(self, *a):
        pass


HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
