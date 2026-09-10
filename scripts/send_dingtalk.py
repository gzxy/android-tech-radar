#!/usr/bin/env python3

import json
import os
import sys
import urllib.request


def send_markdown(title: str, text: str):
    webhook = os.environ["DINGTALK_WEBHOOK"]

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text,
        },
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(
        webhook,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        result = response.read().decode("utf-8")

    print(result)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: send_dingtalk.py <title> <markdown_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    title = sys.argv[1]
    markdown_file = sys.argv[2]

    with open(markdown_file, "r", encoding="utf-8") as f:
        content = f.read()

    send_markdown(title, content)