#!/usr/bin/env python3
"""Publish a `node.invoke_native` to HANA's MQ queue, standing in for a skill.

Why this exists: until NeonGeckoCom/neon-messagebus-mq-connector#66 merges,
the connector's `register_bus_handlers` whitelist drops `node.invoke_native`,
so a skill's emission never reaches HANA. This publishes to the same queue
the connector would, letting the whole Node-side path be exercised without
the skill or the connector fix.

It also stays useful after #66 lands: it isolates the app from the skill, so
a failure here is unambiguously ours.

Usage:
    python scripts/inject_invoke_native.py --session <session_id> --action launch_camera_app
    python scripts/inject_invoke_native.py --session <id> --action launch_email_app \
        --param subject="Running late" --param body="Be there soon"

Find the session id in HANA's logs on Node connect ("Client connected" /
node.hello handling), or in the Node app's Debug Console.

Requires the same MQ credentials HANA uses -- point at them with
NEON_CONFIG_PATH, or pass --host/--port/--user/--password explicitly.
"""

import argparse
import json
import sys
from time import time
from uuid import uuid4

try:
    import pika
except ImportError:
    sys.exit("pika is required: pip install pika")

VHOST = "/neon_chat_api"

VALID_ACTIONS = (
    "launch_camera_app",
    "launch_voice_recorder_app",
    "launch_reminders_app",
    "launch_clock_app",
    "launch_sms_app",
    "launch_email_app",
)


def build_message(session_id: str, action: str, params: dict) -> dict:
    """Mirror what a skill emits: action in data, session in context.

    HANA routes to the right socket by `context.session.session_id`, so that
    field is what actually determines delivery.
    """
    data = {"action": action}
    if params:
        data["params"] = params
    return {
        "msg_type": "node.invoke_native",
        "data": data,
        "context": {
            "session": {"session_id": session_id},
            "ident": str(time()),
            "mq": {"message_id": str(uuid4())},
        },
    }


def publish(message: dict, queue: str, host: str, port: int,
            user: str, password: str) -> None:
    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port, virtual_host=VHOST,
                                  credentials=credentials))
    try:
        channel = connection.channel()
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(content_type="application/json"),
        )
    finally:
        connection.close()


def parse_params(raw: list) -> dict:
    params = {}
    for item in raw or []:
        if "=" not in item:
            sys.exit(f"--param expects key=value, got: {item}")
        key, value = item.split("=", 1)
        params[key] = value
    return params


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--session", required=True,
                        help="Target Node's session_id")
    parser.add_argument("--action", required=True, choices=VALID_ACTIONS)
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Payload param (sms/email only); repeatable")
    parser.add_argument("--queue", required=True,
                        help="HANA's MQ queue -- its `uid`, the routing_key it "
                             "stamps on outbound messages")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5672)
    parser.add_argument("--user", default="neon_api_utils")
    parser.add_argument("--password", default="Klatchat2021")
    args = parser.parse_args()

    params = parse_params(args.param)
    if params and args.action not in ("launch_sms_app", "launch_email_app"):
        print(f"warning: v1 ignores params for {args.action} (launch-only)",
              file=sys.stderr)

    message = build_message(args.session, args.action, params)
    print(json.dumps(message, indent=2))
    publish(message, args.queue, args.host, args.port, args.user, args.password)
    print(f"\npublished to {args.queue!r} on {args.host}:{args.port}{VHOST}")
    print("expect: the Node opens the app, then emits "
          "node.invoke_native.response back to the bus")


if __name__ == "__main__":
    main()
