# claude-code-el-sendgrid

Community event source for [claude-code-event-listeners](https://github.com/mividtim/claude-code-event-listeners) that receives inbound emails via SendGrid's Inbound Parse webhook.

## Install

```bash
git clone https://github.com/mividtim/claude-code-el-sendgrid.git
/el:register ./claude-code-el-sendgrid/sendgrid.sh
```

## Prerequisites

- **SendGrid account** with Inbound Parse configured
- **ngrok** (or similar) forwarding to localhost on the listener port
- SendGrid Inbound Parse webhook URL pointed at the ngrok tunnel

### SendGrid Inbound Parse Setup

1. Go to SendGrid > Settings > Inbound Parse
2. Add a hostname and URL (your ngrok URL)
3. Check "POST the raw, full MIME message" if you want full headers
4. Set up an MX record for your domain pointing to `mx.sendgrid.net`

See [SendGrid docs](https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook) for details.

## Usage

```
/el:listen sendgrid
```

Or with explicit port:

```
/el:listen sendgrid 9998
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SENDGRID_WATERMARK_FILE` | `/tmp/sendgrid-webhook-watermark` | File storing the last processed message ID |

## Output Format

```json
{"from": "jason@example.com", "to": "ghostwriter@yourdomain.com", "subject": "Re: Chapter draft", "text": "Proceed to the 1940s.", "message_id": "<abc123@mail.gmail.com>"}
```

## Requirements

- [claude-code-event-listeners](https://github.com/mividtim/claude-code-event-listeners) plugin installed
- Python 3
- ngrok or similar tunnel (running separately)

## License

MIT
