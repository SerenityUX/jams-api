from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

import jamsapi.openai.auth as openai_auth
import jamsapi.openai.tokens as openai_tokens

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# * Slash Commands
@app.command("/openai-token")
def openai_token(ack, respond, command):
    ack()
    slack_id = command["user_id"]

    if openai_tokens.get_token_by_slack_id(slack_id) is None:
        respond("You don't have a token yet. Please create one.")

    else:
        token = openai_tokens.get_token_by_slack_id(slack_id)
        # Create a datetime object
        date = token.expires_at
        # Format the date into a string
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
        respond(
            f"Your token is `{token.token}`, uses left: *{token.uses_left}* and expires on *{date}*."
        )


@app.command("/openai-create-token")
def openai_create_token(ack, respond, command):
    ack()
    slack_id = command["user_id"]

    if openai_tokens.get_token_by_slack_id(slack_id) is not None:
        respond("You already have a token. Please use that instead.")

    else:
        openai_auth.create_token(slack_id)
        token = openai_tokens.get_token_by_slack_id(slack_id)
        # Create a datetime object
        date = token.expires_at
        # Format the date into a string
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
        respond(f"Your token is `{token.token}`. It expires on *{date}*.")


@app.command("/openai-revoke-token")
def openai_revoke_token(ack, respond, command):
    ack()
    slack_id = command["user_id"]

    if openai_tokens.get_token_by_slack_id(slack_id) is None:
        respond("You don't have a token yet. Please create one.")

    else:
        # Todo: Add confirmation
        openai_auth.revoke_token(slack_id)
        respond("Your token has been revoked.")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
