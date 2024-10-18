import os
import json
import logging
from typing import Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SlackNode:
    def __init__(self):
        logger.info("Initializing SlackNode")

    def extract_text(self, input_text: str) -> str:
        """
        Extract the actual text string from various possible input formats.
        """
        try:
            parsed = json.loads(input_text)
            if isinstance(parsed, dict):
                return str(parsed.get('value', input_text))
            elif isinstance(parsed, str):
                return parsed
        except json.JSONDecodeError:
            pass
        return input_text

    def resolve_path_placeholders(self, text: str, node_data: Dict[str, Any]) -> str:
        """
        Resolve any path placeholders in the input text before processing.
        """
        pattern = re.compile(r"\{\{(.*?)\}\}")
        matches = pattern.findall(text)
        
        for match in matches:
            parts = match.split('.')
            node_id = parts[0]
            path = '.'.join(parts[1:])
            value = self.fetch_value(node_id, path, node_data)
            if value is not None:
                text = text.replace(f"{{{{{match}}}}}", str(value))
        
        return text

    def fetch_value(self, node_id: str, path: str, node_data: Dict[str, Any]) -> Any:
        """
        Fetch the value from the node_data based on the node_id and path.
        """
        try:
            node_result = node_data.get('input', {}).get('result', {})
            for part in path.split('.'):
                node_result = node_result.get(part, None)
                if node_result is None:
                    break
            return node_result
        except Exception as e:
            logger.error(f"Failed to fetch value for {node_id}.{path}: {str(e)}")
            return None

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of SlackNode")
        logger.info(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")
        
        slack_token = node_data.get('slack_token')
        channel = node_data.get('channel')
        message = node_data.get('message')

        if not slack_token:
            logger.error("Missing Slack token")
            return {"status": "error", "message": "Missing Slack token"}

        if not channel:
            logger.error("Missing channel")
            return {"status": "error", "message": "Missing channel"}

        if not message:
            logger.error("Missing message")
            return {"status": "error", "message": "Missing message"}

        try:
            # Resolve any placeholders in the message before sending
            resolved_message = self.resolve_path_placeholders(message, node_data)
            logger.info(f"Resolved message: {resolved_message}")

            # Extract the actual text string
            actual_message = self.extract_text(resolved_message)
            logger.info(f"Extracted message: {actual_message}")

            client = WebClient(token=slack_token)
            response = client.chat_postMessage(channel=channel, text=actual_message)

            result = {
                "status": "success",
                "result": {
                    "message": "Message sent successfully",
                    "ts": response['ts'],
                    "channel": response['channel']
                }
            }
            logger.info(f"Execution completed successfully. Result: {json.dumps(self.log_safe_node_data(result), indent=2)}")
            return result

        except SlackApiError as e:
            error_msg = f"Slack API error: {e.response['error']}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            safe_data = {k: ('[REDACTED]' if k == 'slack_token' else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return safe_data

SlackNodeNode = SlackNode

if __name__ == "__main__":
    test_data = {
        "slack_token": os.environ.get("SLACK_TOKEN"),
        "channel": "#general",
        "message": "Hello from SlackNode!"
    }

    node = SlackNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))