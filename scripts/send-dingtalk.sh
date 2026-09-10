#!/bin/bash

set -e

REPORT_FILE="$1"

if [ -z "$REPORT_FILE" ]; then
    echo "Usage: ./scripts/send-dingtalk.sh <report-file>"
    exit 1
fi

if [ ! -f "$REPORT_FILE" ]; then
    echo "Report file not found: $REPORT_FILE"
    exit 1
fi

if [ -z "$DINGTALK_WEBHOOK" ]; then
    echo "DINGTALK_WEBHOOK is not set"
    exit 1
fi

python3 scripts/send_dingtalk.py \
    "Android Security Audit" \
    "$REPORT_FILE"