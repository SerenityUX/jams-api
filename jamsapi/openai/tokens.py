from pyairtable.orm import Model, fields as F
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Initialize Airtable API
airtable_api_key = os.getenv("AIRTABLE_API_KEY")
airtable_base_key = os.getenv("AIRTABLE_BASE_KEY")


class OpenAIToken(Model):
    token = F.TextField("Token")
    slack_id = F.TextField("Slack ID")
    status = F.SelectField("Status")
    expires_at = F.DatetimeField("ExpirationTime")
    uses_left = F.IntegerField("UsesLeft")

    class Meta:
        table_name = "OpenAI Tokens"
        api_key = airtable_api_key
        base_id = airtable_base_key

    def __str__(self):
        return self.token

    def __repr__(self):
        return self.token


def create_token(token, slack_id, status, expires_at, uses_left):
    tokenish = OpenAIToken(
        token=token,
        slack_id=slack_id,
        status=status,
        expires_at=expires_at,
        uses_left=uses_left,
    )

    tokenish.save()


def get_token(token):
    #! This is a very inefficient way to do this, but I don't know how to do it better with pyairtable at the moment :(
    tokens = OpenAIToken.all()
    for t in tokens:
        if t.token == token and t.status == "Active" and t.expires_at > datetime.now() and t.uses_left > 0:
            return t
    return None


def get_token_by_slack_id(slack_id):
    #! This is a very inefficient way to do this, but I don't know how to do it better with pyairtable at the moment :(
    tokens = OpenAIToken.all()
    for t in tokens:
        if t.slack_id == slack_id and t.status == "Active" and t.expires_at > datetime.now() and t.uses_left > 0:
            return t
    return None


def get_all_tokens():
    return OpenAIToken.all()


def update_token(token, slack_id, status, expires_at, uses_left):
    token = get_token(token)
    token.slack_id = slack_id
    token.status = status
    token.expires_at = expires_at
    token.uses_left = uses_left
    token.save()


def delete_token(token):
    token = get_token(token)
    token.delete()
