from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ai_processor import AIProcessor
import os
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])
processor = AIProcessor()

@app.command("/resolve-incident")
def handle_incident(ack, say, command):
    ack()
    error_message = command["text"]
    solution = processor.generate_solution(error_message)
    
    say(blocks=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Error:* {error_message}"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": solution
            }
        }
    ])

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()