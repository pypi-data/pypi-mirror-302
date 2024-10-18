import logging
from typing import Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

logger = logging.getLogger(__name__)

class SlackNode:
    def __init__(self):
        logger.info("Initializing SlackNode")
        slack_token = os.environ.get('SLACK_BOT_TOKEN')
        if not slack_token:
            raise ValueError("SLACK_BOT_TOKEN environment variable not set")
        self.client = WebClient(token=slack_token)

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        operation = node_data.get('operation')
        channel_id = node_data.get('channel_id')
        if not channel_id:
            raise ValueError("channel_id not specified in node configuration")
        
        if operation == 'sendMessage':
            return self.send_message(node_data, channel_id)
        elif operation == 'receiveMessage':
            return self.receive_message(node_data, channel_id)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def send_message(self, node_data: Dict[str, Any], channel_id: str) -> Dict[str, Any]:
        message = node_data.get('message', 'Hello from SlackNode!')
        try:
            response = self.client.chat_postMessage(channel=channel_id, text=message)
            return {"status": "success", "message": "Message sent", "data": response.data}
        except SlackApiError as e:
            return {"status": "error", "message": f"Slack API error: {e.response['error']}", "data": None}

    def receive_message(self, node_data: Dict[str, Any], channel_id: str) -> Dict[str, Any]:
        # Implement logic to receive messages from Slack
        # This may involve setting up event listeners or using the Real Time Messaging API
        return {"status": "success", "message": "Received message", "data": {}}
