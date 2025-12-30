"""Event emission utilities for EventBridge and SNS"""
import json
import os
import boto3
from .responses import decimal_default


eb = boto3.client("events")
sns = boto3.client("sns")
TOPIC = os.environ.get("SNS_TOPIC_ARN", "")


def _emit(detail_type, detail):
    """Emit events to EventBridge and SNS (best-effort)"""
    # Best-effort: events + demo notifications
    try:
        eb.put_events(Entries=[{
            "Source": "silvermoat.mvp",
            "DetailType": detail_type,
            "Detail": json.dumps(detail, default=decimal_default)
        }])
    except Exception:
        pass

    if TOPIC:
        try:
            sns.publish(TopicArn=TOPIC, Subject=detail_type, Message=json.dumps(detail, default=decimal_default))
        except Exception:
            pass
