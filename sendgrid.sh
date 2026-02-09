#!/bin/bash
# sendgrid — One-shot SendGrid Inbound Parse webhook listener for Claude Code.
#
# Community event source for claude-code-event-listeners.
# Install: /el:register ./sendgrid.sh
#
# Listens on 0.0.0.0:PORT for SendGrid Inbound Parse webhook POSTs.
# Outputs clean email JSON to stdout on the first inbound email, then exits.
#
# Args: [port=9998]
# Env:  SENDGRID_WATERMARK_FILE (default: /tmp/sendgrid-webhook-watermark)
#
# Requires: python3, ngrok running separately (forwarding to PORT)
#
# Setup: Configure SendGrid Inbound Parse to POST to your ngrok URL.
#        See: https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook
#
# Event Source Protocol:
#   Blocks until an email arrives.
#   Outputs JSON: {"from": "...", "to": "...", "subject": "...", "text": "...", ...}

set -euo pipefail

# Resolve through symlinks so companion files are found when registered via el
SCRIPT_DIR="$(cd "$(dirname "$(readlink "$0" 2>/dev/null || echo "$0")")" && pwd)"

PORT="${1:-9998}"

exec python3 "$SCRIPT_DIR/sendgrid-listener.py" "$PORT"
