import jamsapi.openai.tokens as openai_tokens
from datetime import datetime, timedelta
import string
import random

N = 64


def validate_token(token):
    token = openai_tokens.get_token(token)
    if token is None:
        return False
    elif (
        token.status == "Active"
        and token.uses_left > 0
        and token.expires_at > datetime.now()
    ):
        return True
    else:
        return False


def use_token(token):
    if not validate_token(token):
        if token.uses_left == 0:
            token.status = "Expired"

        if token.expires_at < datetime.now():
            token.status = "Expired"

        token.save()

        return False

    token = openai_tokens.get_token(token)

    if token.uses_left == 1:
        token.status = "Expired"

    token.uses_left -= 1
    token.save()

    if token.last_reset < datetime.now() - timedelta(days=30):
        token.uses_left = 500
        token.last_reset = datetime.now()
        token.save()

    return True


def get_token_status(token):
    if not validate_token(token):
        return False
    token = openai_tokens.get_token(token)

    return token.status


def get_token_uses_left(token):
    if not validate_token(token):
        return False
    token = openai_tokens.get_token(token)

    return token.uses_left


def get_token_expires_at(token):
    if not validate_token(token):
        return False
    token = openai_tokens.get_token(token)

    return token.expires_at


def get_token_slack_id(token):
    if not validate_token(token):
        return False
    token = openai_tokens.get_token(token)

    return token.slack_id


def create_token(slack_id):
    token = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))

    uses_left = 500

    last_token = openai_tokens.get_last_revoked_token_by_slack_id(slack_id)

    if last_token is not None:
        uses_left = last_token.uses_left

    openai_tokens.create_token(
        token=token,
        slack_id=slack_id,
        status="Active",
        expires_at=datetime.now() + timedelta(days=30),
        uses_left=uses_left,
    )
    return token


def revoke_token(slack_id):
    token = openai_tokens.get_token_by_slack_id(slack_id)
    token.status = "Revoked"
    token.save()
